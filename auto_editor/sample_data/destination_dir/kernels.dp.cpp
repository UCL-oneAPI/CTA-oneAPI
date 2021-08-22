#include <CL/sycl.hpp>
#include <dpct/dpct.hpp>
/*
 * Copyright (c) 2020-2021, NVIDIA CORPORATION.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*
* Kernel distributes exact part of the kernel shap dataset
* Each block scatters the data of a row of `observations` into the (number of rows of
* background) in `dataset`, based on the row of `X`.
* So, given:
* background = [[0, 1, 2],
                [3, 4, 5]]
* observation = [100, 101, 102]
* X = [[1, 0, 1],
*      [0, 1, 1]]
*
* dataset (output):
* [[100, 1, 102],
*  [100, 4, 102]
*  [0, 101, 102],
*  [3, 101, 102]]
*
*
*/

template <typename DataT, typename IdxT>
void exact_rows_kernel(float* X, const IdxT nrows_X, const IdxT ncols,
                                  const DataT* background, const IdxT nrows_background,
                                  DataT* dataset, const DataT* observation,
                                  sycl::nd_item<3> item_ct1) {
  // Each block processes one row of X. Columns are iterated over by blockDim.x at a time to ensure data coelescing
  int col = item_ct1.get_local_id(2);
  int row = item_ct1.get_group(2) * ncols;

  while (col < ncols) {
    // Load the X idx for the current column
    int curr_X = (int)X[row + col];

    // Iterate over nrows_background
    for (int row_idx = item_ct1.get_group(2) * nrows_background;
         row_idx < item_ct1.get_group(2) * nrows_background + nrows_background;
         row_idx += 1) {
      if (curr_X == 0) {
        dataset[row_idx * ncols + col] =
          background[(row_idx % nrows_background) * ncols + col];
      } else {
        dataset[row_idx * ncols + col] = observation[col];
      }
    }
    // Increment the column
    col += item_ct1.get_local_range().get(2);
  }
}

/*
* Kernel distributes sampled part of the kernel shap dataset
* The first thread of each block calculates the sampling of `k` entries of `observation`
* to scatter into `dataset`. Afterwards each block scatters the data of a row of `X` into the (number of rows of
* background) in `dataset`.
* So, given:
* background = [[0, 1, 2, 3],
                [5, 6, 7, 8]]
* observation = [100, 101, 102, 103]
* nsamples = [3, 2]
*
* X (output)
*      [[1, 0, 1, 1],
*       [0, 1, 1, 0]]
*
* dataset (output):
* [[100, 1, 102, 103],
*  [100, 6, 102, 103]
*  [0, 101, 102, 3],
*  [5, 101, 102, 8]]
*
*
*/

double LCG_random_double(uint64_t * seed)
{
  const uint64_t m = 9223372036854775808ULL; // 2^63
  const uint64_t a = 2806196910506780709ULL;
  const uint64_t c = 1ULL;
  *seed = (a * (*seed) + c) % m;
  return (double) (*seed) / (double) m;
}  

template <typename DataT, typename IdxT>
void sampled_rows_kernel(const IdxT* nsamples, float* X, const IdxT nrows_X,
                                    const IdxT ncols, DataT* background,
                                    const IdxT nrows_background, DataT* dataset,
                                    const DataT* observation, uint64_t seed,
                                    sycl::nd_item<3> item_ct1) {
  // int tid = threadIdx.x + blockIdx.x * blockDim.x;
  // see what k this block will generate
  int k_blk = nsamples[item_ct1.get_group(2)];

  // First k threads of block generate samples
  if (item_ct1.get_local_id(2) < k_blk) {
    int rand_idx = (int)(LCG_random_double(&seed) * ncols);

    // Since X is initialized to 0, we quickly check for collisions (if k_blk << ncols the likelyhood of collisions is low)
    while (dpct::atomic_exchange(
               &(X[2 * item_ct1.get_group(2) * ncols + rand_idx]), (float)1) ==
           1) {
      rand_idx = (int)(LCG_random_double(&seed) * ncols);
    }
  }
  /*CTA1065:count number: recommended to ignore this warning. but you can also consider replacing 'item_ct1.barrier();' with 'item_ct1.barrier(sycl::access::fence_space::local_space);'*/
  item_ct1.barrier();

  // Each block processes one row of X. Columns are iterated over by blockDim.x at a time to ensure data coelescing
  int col_idx = item_ct1.get_local_id(2);
  while (col_idx < ncols) {
    // Load the X idx for the current column
    int curr_X = (int)X[2 * item_ct1.get_group(2) * ncols + col_idx];
    X[(2 * item_ct1.get_group(2) + 1) * ncols + col_idx] = 1 - curr_X;

    for (int bg_row_idx = 2 * item_ct1.get_group(2) * nrows_background;
         bg_row_idx <
         2 * item_ct1.get_group(2) * nrows_background + nrows_background;
         bg_row_idx += 1) {
      if (curr_X == 0) {
        dataset[bg_row_idx * ncols + col_idx] =
          background[(bg_row_idx % nrows_background) * ncols + col_idx];
      } else {
        dataset[bg_row_idx * ncols + col_idx] = observation[col_idx];
      }
    }

    for (int bg_row_idx = (2 * item_ct1.get_group(2) + 1) * nrows_background;
         bg_row_idx <
         (2 * item_ct1.get_group(2) + 1) * nrows_background + nrows_background;
         bg_row_idx += 1) {
      if (curr_X == 0) {
        dataset[bg_row_idx * ncols + col_idx] = observation[col_idx];
      } else {
        // if(threadIdx.x == 0) printf("tid bg_row_idx: %d %d\n", tid, bg_row_idx);
        dataset[bg_row_idx * ncols + col_idx] =
          background[(bg_row_idx) % nrows_background * ncols + col_idx];
      }
    }

    col_idx += item_ct1.get_local_range().get(2);
  }
}

template <typename DataT, typename IdxT>
void kernel_dataset(float* X, 
                    const IdxT nrows_X,
                    const IdxT ncols,
                    DataT* background,
                    const IdxT nrows_background,
                    DataT* dataset,
                    DataT* observation,
                    int* nsamples,
                    const int len_samples, 
                    const int maxsample, 
                    const uint64_t seed)
{
  dpct::device_ext &dev_ct1 = dpct::get_current_device();
  sycl::queue &q_ct1 = dev_ct1.default_queue();

  IdxT nblks;
  IdxT nthreads;

  nthreads = std::min(256, ncols);
  nblks = nrows_X - len_samples;
  printf("nblks = %d len_samples = %d\n", nblks, len_samples );

  if (nblks > 0) {
    /*
    DPCT1049:1: The workgroup size passed to the SYCL kernel may exceed the
    limit. To get the device limit, query info::device::max_work_group_size.
    Adjust the workgroup size if needed.
    */
    q_ct1.submit([&](sycl::handler &cgh) {
      cgh.parallel_for(sycl::nd_range<3>(nblks * nthreads, nthreads),
                       [=](sycl::nd_item<3> item_ct1) {
                         exact_rows_kernel(X, nrows_X, ncols, background,
                                           nrows_background, dataset,
                                           observation, item_ct1);
                       });
    });
  }

  //CUDA_CHECK(cudaPeekAtLastError());

  // check if random part of the dataset is needed
  if (len_samples > 0) {
    nblks = len_samples / 2;
    // each block does a sample and its compliment
    /*
    DPCT1049:2: The workgroup size passed to the SYCL kernel may exceed the
    limit. To get the device limit, query info::device::max_work_group_size.
    Adjust the workgroup size if needed.
    */
    q_ct1.submit([&](sycl::handler &cgh) {
      auto X_nrows_X_len_samples_ncols_ct1 =
          &X[(nrows_X - len_samples) * ncols];
      auto dataset_nrows_X_len_samples_nrows_background_ncols_ct6 =
          &dataset[(nrows_X - len_samples) * nrows_background * ncols];

      cgh.parallel_for(
          sycl::nd_range<3>(nblks * nthreads, nthreads),
          [=](sycl::nd_item<3> item_ct1) {
            sampled_rows_kernel(
                nsamples, X_nrows_X_len_samples_ncols_ct1, len_samples, ncols,
                background, nrows_background,
                dataset_nrows_X_len_samples_nrows_background_ncols_ct6,
                observation, seed, item_ct1);
          });
    });
  }

  //CUDA_CHECK(cudaPeekAtLastError());
}

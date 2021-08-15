#include <CL/sycl.hpp>
#include <dpct/dpct.hpp>
#include <stdio.h>
#include "../common.h"
#include "../util/timer/timer.h"
#include "./kernel.dp.cpp"
#include "./kernel_wrapper.h"        // (in current directory)

void 
kernel_wrapper(record *records,
    long records_mem,
    knode *knodes,
    long knodes_elem,
    long knodes_mem,

    int order,
    long maxheight,
    int count,

    long *currKnode,
    long *offset,
    int *keys,
    record *ans)
{
 dpct::device_ext &dev_ct1 = dpct::get_current_device();
 sycl::queue &q_ct1 = dev_ct1.default_queue();

  long long offload_start = get_time();

  int numBlocks;
  numBlocks = count;                  // max # of blocks can be 65,535
  int threadsPerBlock;
  threadsPerBlock = order < 256 ? order : 256;

  printf("# of blocks = %d, # of threads/block = %d (ensure that device can handle)\n", numBlocks, threadsPerBlock);

  //==================================================50
  //  recordsD
  //==================================================50

  record *recordsD;
  recordsD = (record *)sycl::malloc_device(records_mem, q_ct1);

  //==================================================50
  //  knodesD
  //==================================================50

  knode *knodesD;
  knodesD = (knode *)sycl::malloc_device(knodes_mem, q_ct1);

  //==================================================50
  //  currKnodeD
  //==================================================50

  long *currKnodeD;
  currKnodeD = sycl::malloc_device<long>(count, q_ct1);

  //==================================================50
  //  offsetD
  //==================================================50

  long *offsetD;
  offsetD = sycl::malloc_device<long>(count, q_ct1);

  //==================================================50
  //  keysD
  //==================================================50

  int *keysD;
  keysD = sycl::malloc_device<int>(count, q_ct1);

  //==================================================50
  //  ansD
  //==================================================50

  record *ansD;
  ansD = sycl::malloc_device<record>(count, q_ct1);

  //==================================================50
  //  recordsD
  //==================================================50

  q_ct1.memcpy(recordsD, records, records_mem);

  //==================================================50
  //  knodesD
  //==================================================50

  q_ct1.memcpy(knodesD, knodes, knodes_mem);

  //==================================================50
  //  currKnodeD
  //==================================================50

  q_ct1.memcpy(currKnodeD, currKnode, count * sizeof(long));

  //==================================================50
  //  offsetD
  //==================================================50

  q_ct1.memcpy(offsetD, offset, count * sizeof(long));

  //==================================================50
  //  keysD
  //==================================================50

  q_ct1.memcpy(keysD, keys, count * sizeof(int));

  //==================================================50
  //  ansD
  //==================================================50

  q_ct1.memcpy(ansD, ans, count * sizeof(record));

  //======================================================================================================================================================150
  // findK kernel
  //======================================================================================================================================================150

  /*
  DPCT1049:2: The workgroup size passed to the SYCL kernel may exceed the limit.
  To get the device limit, query info::device::max_work_group_size. Adjust the
  workgroup size if needed.
  */
  q_ct1.submit([&](sycl::handler &cgh) {
    cgh.parallel_for(
        sycl::nd_range<3>(sycl::range<3>(1, 1, numBlocks) *
                              sycl::range<3>(1, 1, threadsPerBlock),
                          sycl::range<3>(1, 1, threadsPerBlock)),
        [=](sycl::nd_item<3> item_ct1) {
          findK(maxheight, knodesD, knodes_elem, recordsD, currKnodeD, offsetD,
                keysD, ansD, item_ct1);
        });
  });

  //==================================================50
  //  ansD
  //==================================================50

  q_ct1.memcpy(ans, ansD, count * sizeof(record)).wait();

  sycl::free(recordsD, q_ct1);
  sycl::free(knodesD, q_ct1);
  sycl::free(currKnodeD, q_ct1);
  sycl::free(offsetD, q_ct1);
  sycl::free(keysD, q_ct1);
  sycl::free(ansD, q_ct1);

  long long offload_end = get_time();

#ifdef DEBUG
  for (int i = 0; i < count; i++)
    printf("ans[%d] = %d\n", i, ans[i].value);
  printf("\n");
#endif

  printf("Total time:\n");
  printf("%.12f s\n", (float) (offload_end-offload_start) / 1000000); 
}

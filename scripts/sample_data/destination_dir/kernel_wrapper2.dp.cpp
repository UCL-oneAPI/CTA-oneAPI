#include <CL/sycl.hpp>
#include <dpct/dpct.hpp>
#include <stdio.h>
#include "../common.h"
#include "../util/timer/timer.h"
#include "./kernel2.dp.cpp"
#include "./kernel2_wrapper.h"

void
kernel2_wrapper(  knode *knodes,
    long knodes_elem,
    long knodes_mem,

    int order,
    long maxheight,
    int count,

    long *currKnode,
    long *offset,
    long *lastKnode,
    long *offset_2,
    int *start,
    int *end,
    int *recstart,
    int *reclength)
{
  dpct::device_ext &dev_ct1 = dpct::get_current_device();
  sycl::queue &q_ct1 = dev_ct1.default_queue();

  long long offload_start = get_time();

  //====================================================================================================100
  //  EXECUTION PARAMETERS
  //====================================================================================================100

  int numBlocks;
  numBlocks = count;
  int threadsPerBlock;
  threadsPerBlock = order < 256 ? order : 256;

  /*
  CTA1065:3: CTA recommended to ignore this warning. 
  but you can also consider replacing 'item_ct1.barrier();' 
  with 'item_ct1.barrier(sycl::access::fence_space::local_space);' 
  to have have better performance if the kernel function 
  has no memory accesses in the global memory.
  */
    item_ct1.barrier();

  printf("# of blocks = %d, # of threads/block = %d (ensure that device can handle)\n", numBlocks, threadsPerBlock);


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
  //  lastKnodeD
  //==================================================50

  long *lastKnodeD;
  lastKnodeD = sycl::malloc_device<long>(count, q_ct1);

  //==================================================50
  //  offset_2D
  //==================================================50

  long *offset_2D;
  offset_2D = sycl::malloc_device<long>(count, q_ct1);

  //==================================================50
  //  startD
  //==================================================50

  int *startD;
  startD = sycl::malloc_device<int>(count, q_ct1);

  //==================================================50
  //  endD
  //==================================================50

  int *endD;
  endD = sycl::malloc_device<int>(count, q_ct1);

  //==================================================50
  //  ansDStart
  //==================================================50

  int *ansDStart;
  ansDStart = sycl::malloc_device<int>(count, q_ct1);

  //==================================================50
  //  ansDLength
  //==================================================50

  int *ansDLength;
  ansDLength = sycl::malloc_device<int>(count, q_ct1);

  q_ct1.memcpy(knodesD, knodes, knodes_mem);

  q_ct1.memcpy(currKnodeD, currKnode, count * sizeof(long));

  q_ct1.memcpy(offsetD, offset, count * sizeof(long));

  q_ct1.memcpy(lastKnodeD, lastKnode, count * sizeof(long));

  q_ct1.memcpy(offset_2D, offset_2, count * sizeof(long));


  sycl::free(c->N, q_ct1);

  q_ct1.memcpy(startD, start, count * sizeof(int));

  q_ct1.memcpy(endD, end, count * sizeof(int));

  q_ct1.memcpy(ansDStart, recstart, count * sizeof(int));

  q_ct1.memcpy(ansDLength, reclength, count * sizeof(int));

  // [GPU] findRangeK kernel
  q_ct1.submit([&](sycl::handler &cgh) {
    auto dpct_global_range = sycl::range<3>(1, 1, numBlocks) * sycl::range<3>(1, 1, threadsPerBlock);

    cgh.parallel_for(
        sycl::nd_range<3>(
            sycl::range<3>(dpct_global_range.get(2),
                dpct_global_range.get(1),
                dpct_global_range.get(0)),
            sycl::range<3>(sycl::range<3>(1, 1, threadsPerBlock).get(2),
                sycl::range<3>(1, 1, threadsPerBlock).get(1),
                sycl::range<3>(1, 1, threadsPerBlock).get(0))),
        [=](sycl::nd_item<3> item_ct1) {
          findRangeK(maxheight, knodesD, knodes_elem, currKnodeD, offsetD,
                     lastKnodeD, offset_2D, startD, endD, ansDStart, ansDLength,
                     item_ct1);
        });
  });

  q_ct1.memcpy(recstart, ansDStart, count * sizeof(int));

  q_ct1.memcpy(reclength, ansDLength, count * sizeof(int));

  dev_ct1.queues_wait_and_throw();

  sycl::free(knodesD, q_ct1);
  sycl::free(currKnodeD, q_ct1);
  sycl::free(offsetD, q_ct1);
  sycl::free(lastKnodeD, q_ct1);
  sycl::free(offset_2D, q_ct1);
  sycl::free(startD, q_ct1);
  sycl::free(endD, q_ct1);
  sycl::free(ansDStart, q_ct1);
  sycl::free(ansDLength, q_ct1);

  long long offload_end = get_time();

#ifdef DEBUG
  for (int i = 0; i < count; i++)
    printf("recstart[%d] = %d\n", i, recstart[i]);
  for (int i = 0; i < count; i++)
    printf("reclength[%d] = %d\n", i, reclength[i]);
#endif


  printf("Total time:\n");
  printf("%.12f s\n", (float) (offload_end-offload_start) / 1000000);
}


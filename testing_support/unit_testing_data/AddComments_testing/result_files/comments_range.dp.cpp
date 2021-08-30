  q_ct1.memcpy(ansDLength, reclength, count * sizeof(int));

  // [GPU] findRangeK kernel
  /*
  CTA1065:3: CTA recommended to ignore this warning. 
  but you can also consider replacing 'item_ct1.barrier();' 
  with 'item_ct1.barrier(sycl::access::fence_space::local_space);' 
  to have have better performance if the kernel function 
  has no memory accesses in the global memory.
  */
  q_ct1.submit([&](sycl::handler &cgh) {
    cgh.parallel_for(
        sycl::nd_range<3>(blocks * threads, threads),
        [=](sycl::nd_item<3> item_ct1) {
          findRangeK(maxheight, knodesD, knodes_elem, currKnodeD, offsetD,
                     lastKnodeD, offset_2D, startD, endD, ansDStart, ansDLength,
                     item_ct1);
        });
  });

  q_ct1.memcpy(recstart, ansDStart, count * sizeof(int));
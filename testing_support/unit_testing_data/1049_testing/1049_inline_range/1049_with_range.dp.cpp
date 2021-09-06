  q_ct1.memcpy(ansDLength, reclength, count * sizeof(int));

  // [GPU] findRangeK kernel
  /*
  DPCT1049:3: The workgroup size passed to the SYCL kernel may exceed the limit.
  To get the device limit, query info::device::max_work_group_size. Adjust the
  workgroup size if needed.
  */
  q_ct1.submit([&](sycl::handler &cgh) {
    cgh.parallel_for(
        sycl::nd_range<3>(sycl::range<3>(1, 1, numBlocks) *
                              sycl::range<3>(1, 1, threadsPerBlock),
                          sycl::range<3>(1, 1, threadsPerBlock)),
        [=](sycl::nd_item<3> item_ct1) {
          findRangeK(maxheight, knodesD, knodes_elem, currKnodeD, offsetD,
                     lastKnodeD, offset_2D, startD, endD, ansDStart, ansDLength,
                     item_ct1);
        });
  });

  q_ct1.memcpy(recstart, ansDStart, count * sizeof(int));
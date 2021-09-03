  /*
  DPCT1049:1: The workgroup size passed to the SYCL kernel may exceed the limit.
  To get the device limit, query info::device::max_work_group_size. Adjust the
  workgroup size if needed.
  */
  q_ct1.submit([&](sycl::handler &cgh) {
    sycl::accessor<uint8_t, 1, sycl::access::mode::read_write,
                   sycl::access::target::local>
        dpct_local_acc_ct1(sycl::range<1>(sizeof(sycl::uchar4) *
                                          iLocalPixPitch * (iBlockDimY + 2)),
                           cgh);

    cgh.parallel_for(
        sycl::nd_range<3>(gws * lws, lws), [=](sycl::nd_item<3> item_ct1) {
          ckMedian(cmDevBufIn, cmDevBufOut, iLocalPixPitch, uiImageWidth,
                   uiImageHeight, item_ct1, dpct_local_acc_ct1.get_pointer());
        });
  });
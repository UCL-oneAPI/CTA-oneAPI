 /*
DPCT1049:107: The workgroup size passed to the SYCL kernel may exceed the limit.
To get the device limit, query info::device::max_work_group_size. Adjust the
workgroup size if needed.
*/
                        stream->submit([&](sycl::handler &cgh) {
                                auto d_begin_offsets_ct4 = d_begin_offsets;
                                auto d_end_offsets_ct5 = d_end_offsets;
                                auto num_segments_ct6 = num_segments;

                                cgh.parallel_for(
                                    sycl::nd_range<3>(
                                        num_segments *
                                            sycl::range<3>(
                                                1, 1,
                                                pass_config.segmented_config
                                                    .block_threads),
                                        sycl::range<3>(
                                            1, 1,
                                            pass_config.segmented_config
                                                .block_threads)),
                                    [=](sycl::nd_item<3> item_ct1) {
                                            segmented_kernel(
                                                d_keys_in, d_keys_out,
                                                d_values_in, d_values_out,
                                                d_begin_offsets_ct4,
                                                d_end_offsets_ct5,
                                                num_segments_ct6, current_bit,
                                                pass_bits);
                                    });
                        });

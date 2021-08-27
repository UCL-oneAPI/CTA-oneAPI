  CUDA_SAFE_CALL((c->pi = sycl::malloc_device<float>(num_clusters, q_ct1), 0));

  /*
  DPCT1003:43: Migrated API does not return error code. (*, 0) is inserted. You
  may need to rewrite this code.
  */
  CUDA_SAFE_CALL(
      (c->Rinv = (float *)sycl::malloc_device(sizeof(float) * num_dimensions *
                                                  num_dimensions * num_clusters,
                                              q_ct1),
       0));


  CUDA_SAFE_CALL((c->pi = sycl::malloc_device<float>(num_clusters, q_ct1), 0));
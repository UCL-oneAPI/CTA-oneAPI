void bitonic_sort( T* sh_data, const uint localid, sycl::nd_item<3> item_ct1)
{
  for (uint ulevel = 1; ulevel < LQSORT_LOCAL_WORKGROUP_SIZE; ulevel <<= 1) {
    for (uint j = ulevel; j > 0; j >>= 1) {
      uint pos = 2*localid - (localid & (j - 1));

      uint direction = localid & ulevel;
      uint av = sh_data[pos], bv = sh_data[pos + j];
      const bool sortThem = av > bv;
      const uint greater = select(bv, av, sortThem);
      const uint lesser  = select(av, bv, sortThem);

      sh_data[pos]     = select(lesser, greater, direction);
      sh_data[pos + j] = select(greater, lesser, direction);
      /*
      DPCT1065:1: Consider replacing sycl::nd_item::barrier() with
       * sycl::nd_item::barrier(sycl::access::fence_space::local_space) for
       * better performance, if there is no access to global memory.
      */
      item_ct1.barrier();
    }
  }

  for (uint j = LQSORT_LOCAL_WORKGROUP_SIZE; j > 0; j >>= 1) {
    uint pos = 2*localid - (localid & (j - 1));

    uint av = sh_data[pos], bv = sh_data[pos + j];
    const bool sortThem = av > bv;
    sh_data[pos]      = select(av, bv, sortThem);
    sh_data[pos + j]  = select(bv, av, sortThem);

    /*
    DPCT1065:2: Consider replacing sycl::nd_item::barrier() with
     * sycl::nd_item::barrier(sycl::access::fence_space::local_space) for better
     * performance, if there is no access to global memory.
    */
    item_ct1.barrier();
  }
}

  // Allocate memory in the sequence this block is a part of
  if (localid == 0) {
    // get shared variables
    psstart = &pparent->sstart;
    psend = &pparent->send;
    poldstart = &pparent->oldstart;
    poldend = &pparent->oldend;
    pblockcount = &pparent->blockcount;
    // Atomic increment allocates memory to write to.
    /*
    DPCT1039:3: The generated code assumes that "psstart" points to the
     * global memory address space. If it points to a local memory address
     * space, replace "dpct::atomic_fetch_add" with
     * "dpct::atomic_fetch_add<uint,
     * sycl::access::address_space::local_space>".
    */
    *lbeg =
        sycl::atomic<uint>(sycl::global_ptr<uint>(psstart)).fetch_add(*ltsum);
    // Atomic is necessary since multiple blocks access this
    /*
    DPCT1039:4: The generated code assumes that "psend" points to the
     * global memory address space. If it points to a local memory address
     * space, replace "dpct::atomic_fetch_sub" with
     * "dpct::atomic_fetch_sub<uint,
     * sycl::access::address_space::local_space>".
    */
    *gbeg =
        sycl::atomic<uint>(sycl::global_ptr<uint>(psend)).fetch_sub(*gtsum) -
        *gtsum;
  }
}

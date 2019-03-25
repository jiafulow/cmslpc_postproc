python cmslpc_postproc/hadd_npz.py -f histos_tba_add.npz PostProcessDAGs/jftest1/histos_tba_*.npz
python cmslpc_postproc/hadd_npz.py -f histos_tbd_add.npz PostProcessDAGs/jftest4/histos_tbd_*.npz
python cmslpc_postproc/hadd_npz.py -f histos_tbe_add.npz PostProcessDAGs/jftest5/histos_tbe_*.npz
python cmslpc_postproc/hadd_npz.py -f histos_tba_omtf_add.npz PostProcessDAGs/jftest11/histos_tba_*.npz
python cmslpc_postproc/hadd_npz.py -f histos_tbd_omtf_add.npz PostProcessDAGs/jftest14/histos_tbd_*.npz
python cmslpc_postproc/hadd_npz.py -f histos_tbe_omtf_add.npz PostProcessDAGs/jftest15/histos_tbe_*.npz
python cmslpc_postproc/hadd_npz.py -f histos_tba_run3_add.npz PostProcessDAGs/jftest21/histos_tba_*.npz
python cmslpc_postproc/hadd_npz.py -f histos_tbd_run3_add.npz PostProcessDAGs/jftest24/histos_tbd_*.npz
python cmslpc_postproc/hadd_npz.py -f histos_tbe_run3_add.npz PostProcessDAGs/jftest25/histos_tbe_*.npz

hadd -f histos_tbc_add.root PostProcessDAGs/jftest3/histos_tbc_*.root
hadd -f histos_tbc_omtf_add.root PostProcessDAGs/jftest13/histos_tbc_*.root
hadd -f histos_tbb_add.root PostProcessDAGs/jftest2/histos_tbb_*.root
hadd -f histos_tbb_140_add.root PostProcessDAGs/jftest2_140/histos_tbb_*.root
hadd -f histos_tbb_250_add.root PostProcessDAGs/jftest2_250/histos_tbb_*.root
hadd -f histos_tbb_300_add.root PostProcessDAGs/jftest2_300/histos_tbb_*.root

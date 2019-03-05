rm -rf PostProcessDAGs_old
mv PostProcessDAGs PostProcessDAGs_old
connect shell find /local-scratch/jiafulow/connect-client/ -name "jftest*" -type d -exec rm -rf {} +
python example.py

#cd PostProcessDAGs/jftest1 && connnode && cd -
#cd PostProcessDAGs/jftest4 && connnode && cd -
#cd PostProcessDAGs/jftest11 && connnode && cd -
#cd PostProcessDAGs/jftest14 && connnode && cd -

cd PostProcessDAGs/jftest3 && connnode && cd -
cd PostProcessDAGs/jftest13 && connnode && cd -
cd PostProcessDAGs/jftest2 && connnode && cd -
cd PostProcessDAGs/jftest2_140 && connnode && cd -
cd PostProcessDAGs/jftest2_250 && connnode && cd -
cd PostProcessDAGs/jftest2_300 && connnode && cd -

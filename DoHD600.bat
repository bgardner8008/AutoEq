python -m autoeq --output-dir "output\Harman" --input-file "measurements\oratory1990\data\over-ear\Sennheiser HD 600.csv" --compensation "compensation\harman_over-ear_2018.csv" --parametric-eq --parametric-eq-config "8_PEAKING_WITH_SHELVES"

python EqToTP.py "output\Harman\Sennheiser HD 600\Sennheiser HD 600 ParametricEQ.txt" "output\tp_harman.txt" "harman"

python -m autoeq --output-dir "output\diffuse" --input-file "measurements\oratory1990\data\over-ear\Sennheiser HD 600.csv" --compensation "compensation\diffuse_field_iso_11904-2.csv" --parametric-eq --parametric-eq-config "8_PEAKING_WITH_SHELVES"

python EqToTP.py "output\diffuse\Sennheiser HD 600\Sennheiser HD 600 ParametricEQ.txt" "output\tp_diffuse.txt" "diffuse"


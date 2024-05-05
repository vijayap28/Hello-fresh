python3 -r requirement.txt

Run code,Two ways:

1. Code can be run with command  python3 hf_bi_python_excercise in termianl
2.  cd hf_bi_python_excercise
    python3 main.py


Unit Test Run:
1. cd hf_bi_python_excercise
2. python3 -m unit_test test.py


Note:
1. Output is saved inside recipes_etl folder.
2. I have taken couple of assumptions:
   1.  If both prepTime and cookTime are empty, then difficulty is Unknown. (From assignment, it was not clear)
   2.  Third column in results.csv is total of total_time (which is sum of prepTime and cookTime
   3. Please let me know if you need any changes.

3. I have requirement.txt, please run this file to install all the dependencies.
4. I have added unit test cases for the code.
5. Code is working with all the UT's are running fine with python3.9




# pyfuzzy
Port pyfuzzy on Python3 (include antlr3 v.3.1.4)

# Documentation

* pyfuzzy: http://pyfuzzy.sourceforge.net/
* antlr3: http://www.antlr3.org/

# Installation

Move folders antlr3 and pyfuzzy in %PYTHON_PATH%\site-packages\

# Use

1. Create demo.fcl file in your project with

```
FUNCTION_BLOCK Fuzzy_FB
    VAR_INPUT
        TimeDay : REAL; (* RANGE(0 .. 23) *)
        ApplicateHost: REAL;
    END_VAR

    VAR_OUTPUT
        ProbabilityAccess: REAL;
    END_VAR

    FUZZIFY TimeDay
        TERM inside := (0, 0) (8, 1) (22,0);
        TERM outside := (0, 1) (8, 0) (22, 1);
    END_FUZZIFY

    FUZZIFY ApplicateHost
        TERM few := (0, 1) (100, 0) (200, 0);
        TERM many := (0, 0) (100, 0) (200, 1);
    END_FUZZIFY


    DEFUZZIFY ProbabilityAccess
        TERM hight := 1;
        TERM medium := 0.5;
        TERM low := 0;
        ACCU: MAX;
        METHOD: COGS;
        DEFAULT := 0;
    END_DEFUZZIFY


    RULEBLOCK No1
        AND : MIN;
        RULE 1 : IF TimeDay IS outside AND ApplicateHost IS few THEN ProbabilityAccess IS hight;
        RULE 2 : IF ApplicateHost IS many THEN ProbabilityAccess IS hight;
        RULE 3 : IF TimeDay IS inside AND ApplicateHost IS few THEN ProbabilityAccess IS low;
    END_RULEBLOCK

END_FUNCTION_BLOCK
```

2. Add code below:

```python
import fuzzy.storage.fcl.Reader

system = fuzzy.storage.fcl.Reader.Reader().load_from_file("demo.fcl")

my_input = {
        "TimeDay": 12,
        "ApplicateHost": 20,
        "TimeConfiguration": 5,
        "TimeRequirements": 5
        }
my_output = {
        "ProbabilityDistribution": 0.0,
        "ProbabilityAccess": 0.0
        }
        
system.calculate(my_input, my_output)

print(u"ProbabilityAccess = {0}".format(my_output["ProbabilityAccess"]))

# Output:
# ProbabilityAccess = 0.2857142857142857
```

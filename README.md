# Python backend homework

Python backend homework made with Flask.

## 1. Installation
1. Clone the repository
2. Install requirements
  ```bash
  pip install -r requirements.txt
  ```

## 2. Concerns and solutions
#### 2.1. Unit conversion
   - There are two unit conversion strategies implemented:
       - Manual conversion:
           - faster execution, but less precise
       - Unit conversion using 'pint'
           - https://pypi.org/project/Pint/
           - slower execution, but more precise

#### 2.2. Observations containing multiple values and units

   - There are certain observation types in the input data which contained multiple components with measurement values and units (e.g.: blood pressure) compared to others (e.g.: height) which only contained a single value with a unit.
   In the output format it was indicated when the desired outcome was a list or not and with the `measurementValue` and `measurementUnit` keys a list was not indicated.
   - My solution:

     Not to lose data and stay coherent I always returned a list with the value(s) for the `measurementValue` and a list with the unit(s) for the `measurementUnit` keys in the output.


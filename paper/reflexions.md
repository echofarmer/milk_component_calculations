\# Reflections



Reflections on the modeling units of CMSE 802 and how they connect to my project.



\## Modeling Intro



Class dates: September 8 to 17, 2026. Written: November 22, 2026.



In this unit we started with a script that draws a colored triangle and improved it in small steps. I replaced raw numbers with named variables, turned the script into a function, moved it into its own file (`BTriang.py`), and added a docstring. Three things were new to me: making Git commits properly, using Ruff to find problems in my code, and writing a docstring that I can read back with `help()`. The most useful tool was Git. With `git status` and `git diff` I can see exactly what changed before I save it, and a clear commit message tells me later why I made the change.



I already use these ideas in my milk component project. The code is written as functions in `.py` files, the whole workflow runs from the terminal with `make run`, and `make lint` and `make format` run Ruff on the project. I check `git status` before I commit. After this course I plan to keep using Git for my research code, to run Ruff before I commit, and to write my analysis steps as functions instead of long notebooks. One improvement I still want to make in my project is to give names to the raw numbers, for example the hours 11 and 18 that decide the milking number in `uploading.py`.



\## Analytical Modeling



Class dates: September 22 and 24, 2026.



In this unit we worked with models that are written as equations. With SymPy I solved the doubling time of an exponential model and built a model of caffeine in the blood after three cups of coffee. Then we made "phantom" data from a known model with noise, estimated the parameters by searching for the smallest error, and fitted regression models to a real dataset with statsmodels. The lesson I will remember most is to test a method first on data where the answer is known. In Part 3 the first fit was wrong: the best values sat on the edge of the search range and the error was 120. Because the true model was known, we could see that the equation had the wrong sign, and after the correction the error dropped to 0.66. The most useful tool for me was statsmodels, because the regression summary and the residual plots show how well a model fits, not only one number.



This unit connects to my project in three ways. The center of my project is an analytical formula: yield (kg) = milk (kg) x component percent / 100. In Part 4 we had to decide what to do with missing values and say what we chose. My project does the same with failed samples: they are set to missing and listed in a data-quality report, not dropped silently. I also need regression models with clear assumptions to compare the diets in my trial. In future work I plan to fit curves to my own data (for example a lactation curve), to test new code on invented data before I trust it, to check residual plots, and to use SymPy to check my formulas.



\## Physical Modeling



Class dates: October 13 to 22, 2026. 



In this unit I ran two of the notebooks. The first was the SIR model, which describes an epidemic with three groups (susceptible, infected, and recovered) and the rates of moving between them, and solves the equations with `solve\_ivp`. By changing the rates I could see how the curve of infected individuals changed. The second was the wave equation, where the same simulation is written in plain Python, with NumPy, and with Numba to compare the speed. The point of that comparison is that NumPy runs the loops in compiled code, so the same simulation takes much less time. I did not run the finite-element software (MFEM and BESFEM) on the HPCC. The most useful idea for me was to match the model to the question: rates when a system is described by a few states, a grid when space matters, finite elements for complex shapes, and agents when many individuals interact. A simple model can be the right choice.



This connects to my research in several ways. A model like SIR could describe how a contagious disease spreads in a herd. Heat stress could be described with states and rates, with body temperature rising and falling with the heat load. Whole-farm simulation models such as RuFaS follow the same idea of turning assumptions and rules into simulated results. The speed lesson applies to my sensor data, which has a reading every 10 minutes for each cow, so code that works on whole columns matters. As a next step, I plan to try a small rate model for one research question.



\## Data-Driven Modeling



Class dates: November 3 to 12, 2026. 



In this unit I ran Parts 1 to 3. In Part 1 I downloaded 75 years of daily weather for East Lansing from the Open-Meteo web API and saved the address of the request, the date, and a checksum, so that another person can repeat the download. The annual mean temperature was 9.08 °C, with a 95% confidence interval of 8.89 to 9.28, and the trend was 0.18 °C per decade. We used one value per year because daily values are not independent. In Part 2 I used scikit-learn to split data into training and test sets, to compare a model with a baseline, and to see overfitting. In Part 3 a one-minute TPOT search reached a balanced accuracy of 0.974, almost the same as a simple logistic regression (0.976), and both were far above the baseline of 0.500. I have not yet run Part 4, the Slurm job array on the HPCC. The most useful part for me was getting data from a web API with code and recording where the data came from. I plan to use it for my heat stress trial, to download temperature and humidity for the farm and the trial dates.



The class page for this unit asks three questions about my project.



1\. Which data-driven component could contribute? Classical machine learning. My project calculates yields with a formula from measurements that already exist. A model could answer a different question: can a cow's daily milk yield be predicted from her sensor data (body temperature, activity, and rumination)?

2\. Do I have enough data to trust it? I do not think so. My trial has more than 40 cows. Each cow has thousands of sensor readings, but readings from the same cow are not independent, so the number of cows is what counts, and that is small for a model with several features. To avoid leakage I would split the data by cow, so that all the readings of one cow stay in the same set and the model is tested on cows it has not seen. The baseline to beat would be each cow's own average milk yield.

3\. What evidence would I need, and what would a teammate need? I would need to see that the model predicts well for cows that were not used in training and that it is clearly better than the baseline. A teammate would need the code, the environment file, the random seeds, and a record of where the data came from. Reproducible would be the hardest principle, because the trial data cannot be shared in a public repository and the results depend on the random seeds and the software versions. A concrete step is to save the seed and the package versions with every result, and to keep example data in the same format as the real files.


from flask import Flask, render_template, request

app = Flask(__name__)

PRELIM_PERCENT = 0.2
MIDTERM_PERCENT = 0.3
FINAL_PERCENT = 0.5
PASSING_GRADE =  75

@app.route('/', methods=['GET', 'POST'])
#Input 
def index():
    result = None
    if request.method == 'POST':
        try:
                #Retrieves input values from the form
            prelim_grade = request.form.get('prelim_grade')
            midterm_grade = request.form.get('midterm_grade')
            final_grade = request.form.get('final_grade')

                #If there was no inputs submitted
            if not prelim_grade and not midterm_grade and not final_grade:
                return render_template('index.html', error="Please input grades")
            
            prelim_grade = float(prelim_grade) if prelim_grade else None
            midterm_grade = float(midterm_grade) if midterm_grade else None
            final_grade = float(final_grade) if final_grade else None
            
                #Checking whether inputted grades are in between 0 - 100
            if (prelim_grade is not None and (prelim_grade < 0 or prelim_grade > 100)) or \
               (midterm_grade is not None and (midterm_grade < 0 or midterm_grade > 100)) or \
               (final_grade is not None and (final_grade < 0 or final_grade > 100)):
                return render_template('index.html', error="Please enter valid grades between 0 and 100.")
            
            #Checks if input value is not numerical
        except ValueError:
            return render_template('index.html', error="Please input a numerical value")
        
        result = calculating(prelim_grade, midterm_grade, final_grade)
    
    return render_template('index.html', result=result)

def calculating(prelim_grade=None, midterm_grade=None, final_grade=None):
    
#Formula used (Prelim Grade * Prelim%(20%)) + (Midterm Grade * Midterm(30%)) + (Final Grade * Final(50%)) = Passing Grade(75)
    #If only one single grade was given
    if prelim_grade is not None and midterm_grade is None and final_grade is None:
        required_grade = (PASSING_GRADE - (prelim_grade * PRELIM_PERCENT)) / (MIDTERM_PERCENT + FINAL_PERCENT)
        result = f"You need to have a final grade of {required_grade:.2f} in Midterms and Finals to pass."

    elif prelim_grade is None and midterm_grade is not None and final_grade is None:
        required_grade = (PASSING_GRADE - (midterm_grade * MIDTERM_PERCENT)) / (PRELIM_PERCENT + FINAL_PERCENT)
        result = f"You need to have a final grade of {required_grade:.2f} in Prelims and Finals to pass."

    elif prelim_grade is None and midterm_grade is None and final_grade is not None:
        required_grade = (PASSING_GRADE - (final_grade * FINAL_PERCENT)) / (PRELIM_PERCENT + MIDTERM_PERCENT)
        result = f"You need to have a prelim and midterm average grade of {required_grade:.2f} in Prelims and Midterms to pass."

    #All three grades were given
    elif prelim_grade is not None and midterm_grade is not None and final_grade is not None:
        total_grade = (prelim_grade * PRELIM_PERCENT) + (midterm_grade * MIDTERM_PERCENT) + (final_grade * FINAL_PERCENT)
        if total_grade > 75:
            result = f"You have passed with an overall grade of {total_grade:.2f}."
        else:
            result = f"Your overall grade {total_grade: .2f} did not reach the passing grade 75"
    #If two grades were given
    elif prelim_grade is not None and midterm_grade is not None and final_grade is None:
        total_grade = (PASSING_GRADE - ((prelim_grade * PRELIM_PERCENT) + (midterm_grade * MIDTERM_PERCENT))) / FINAL_PERCENT
        result = f"In order to reach 75 (Passing Grade), you need to have {total_grade: .2f} in Finals"

    elif prelim_grade is not None and midterm_grade is None and final_grade is not None:
        total_grade = (PASSING_GRADE - ((prelim_grade * PRELIM_PERCENT) + (final_grade * FINAL_PERCENT))) / MIDTERM_PERCENT
        result = f"In order to reach 75 (Passing Grade), you need to have {total_grade: .2f} in Midterms"

    elif prelim_grade is None and midterm_grade is not None and final_grade is not None:
        total_grade = (PASSING_GRADE - ((midterm_grade * MIDTERM_PERCENT) + (final_grade * FINAL_PERCENT))) / PRELIM_PERCENT
        result = f"In order to reach 75 (Passing Grade), you need to have {total_grade: .2f} in Prelims"
    
    else:
        return render_template('index.html', f"Please put valid inputs")

    #Returns result to display in front of the student
    return result

if __name__ == '__main__':
    app.run(debug=True)



#Hello, I mostly used ChatGPT to help me creating this simple grade calculator, mostly in knowing how python flask work GET and POST, how to retrieve inputs from html, how to use else, if, elseif, return function, or in general, mostly everything.
#I also used ChatGPT for debugging codes because 
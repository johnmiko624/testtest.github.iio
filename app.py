from flask import Flask, render_template, request

app = Flask(__name__)

# Function to calculate the required Midterm and Final grades
def calculate_grades(prelim):
    prelim_weight = 0.20
    midterm_weight = 0.30
    final_weight = 0.50
    passing_grade = 75.0

    # Calculate the portion of the grade already achieved with the Prelim grade
    current_grade = prelim * prelim_weight

    if current_grade >= passing_grade:
        return "You are already passing based on your Prelim grade alone."

    remaining_grade = passing_grade - current_grade

    # Determine the required midterm and final grades
    required_midterm = remaining_grade / (midterm_weight + final_weight) * midterm_weight
    required_final = remaining_grade / (midterm_weight + final_weight) * final_weight

    return required_midterm, required_final

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error_message = None

    if request.method == 'POST':
        try:
            prelim_grade = float(request.form['prelim_grade'])

            if prelim_grade < 0 or prelim_grade > 100:
                error_message = "Prelim grade must be between 0 and 100."
            else:
                result = calculate_grades(prelim_grade)
                if isinstance(result, tuple):
                    result = (f"To pass, you need at least {result[0]:.2f} in the Midterm "
                              f"and {result[1]:.2f} in the Final.")
                else:
                    result = result

        except ValueError:
            error_message = "Please enter a valid numerical value for the Prelim grade."

    return render_template('index.html', result=result, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)

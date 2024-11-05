import random
import math
from flask import Flask, render_template, request
from formula import start_attempt

app = Flask(__name__)

@app.route('/')
def home():
    message = "Hello World"
    return render_template('index.html', message = message)

@app.route('/result', methods=['POST'])
def result():
    # iterator
    counter = 0

    # pity  counters
    goldPityCount = 0
    purplePityCount = 0
    softPityRate = 0

    # variables for the soft pity calculation
    base_rate = 1.6
    start_attempt = 74
    max_attempt = 90

    # pull counters
    goldCount = 0
    purpleCount = 0
    blueCount = 0
    displayResult = ""

    pullCount = int(request.form['number'])

    def logistic_drop_rate(base_rate, start_attempt, steepness, max_attempt):
        L = 1.0  # Maximum drop rate (100%)
        k = steepness  # Controls the steepness of the curve
        n0 = (max_attempt + start_attempt) / 2  # Midpoint

        # Calculate drop rate using the logistic function
        drop_rate = L / (1 + math.exp(-k * (attempt - n0)))

        # Adjust drop rate based on base rate at the start attempt
        adjusted_rate = drop_rate - (L - 1.6) / (1 + math.exp(-k * (start_attempt - n0)))
        # return max(adjusted_rate, 1.6)

    while counter < pullCount:
        result = round(float(random.random() * 100), 2)

        if counter % 10 == 0:  # adds a line break every 10 pulls
            displayResult += f"\n<p>Multi-pull #{counter // 10 + 1}</p>"

        # guarantees the next pull if pity is hit
        if purplePityCount == 9: result = 13
        if goldPityCount == 89: result = 1.6

        # roll logic
        if goldPityCount >= 74:
            # for attempt in range(goldPityCount, max_attempt + 1):
            #     softPityRate = logistic_drop_rate(base_rate, start_attempt, 1.2, max_attempt)
            # start_attempt += 1
            softPityRate = (goldPityCount - 73) * ((17-(90-goldPityCount)) * 6.25)
            # softPityRate = (goldPityCount - 73) * (0.6 * ((goldPityCount - 73)/2))

        if result <= 1.6 + softPityRate:
            displayResult += f"<p class='gold'>(SSR rate - {round(1.6 + softPityRate, 2)}%) Pull {counter + 1}: 5***** Gold!!! - {result}%</p>"
            goldCount += 1
            softPityRate = 0
            goldPityCount = 0
        elif result <= 13:
            displayResult += f"<p class='purple'>(SSR rate - {round(1.6 + softPityRate, 2)}%) Pull {counter + 1}: 4**** Purple - {result}%</p>"
            purplePityCount = 0
            goldPityCount += 1
            purpleCount += 1
        else:
            displayResult += f"<p class='blue'>(SSR rate - {round(1.6 + softPityRate, 2)}%) Pull {counter + 1}: 3*** Blue - {result}%</p>"
            goldPityCount += 1
            purplePityCount += 1
            blueCount += 1

        counter += 1
    displayResult += f"\n<p>Total number of pulls: {pullCount}</p>"
    displayResult += f"\nGacha results:\n<p class='gold'>5***** Gold count: {goldCount}</p>\n<p class='purple'>4**** Purple count: {purpleCount}</p></p>\n<p class='blue'>3*** Blue count: {blueCount}</p>\n"

    return render_template('result.html', displayResult = displayResult, pullCount = pullCount)


if __name__ == '__main__':
    app.run(debug=True)

# #iterator
# counter = 0
#
# #pity counters
# goldPityCount = 0
# purplePityCount = 0
#
# #pull counters
# goldCount = 0
# purpleCount = 0
# blueCount = 0
#
# #ANSI Escape colors
# gold = "\033[1;33;40m"
# purple = "\033[1;35;40m"
# blue = "\033[1;34;40m"
# white = "\033[1;32;40m"
#
# pullCount = int(input("Enter number of Tickets: "))
#
# while counter < pullCount:
#     result = round(float(random.random()*100), 2)
#
#     if counter % 10 == 0: #adds a line break every 10 pulls
#         print(f"\n{white}Multi-pull #{counter // 10 + 1}")
#
#     #guarantees the next pull if pity is hit
#     if purplePityCount == 9: result = 13
#     if goldPityCount == 89: result = 1.6
#
#     #roll logic
#     if result <= 1.6:
#         print(f"{gold} Pull {counter + 1}: 5***** Gold!!! - {result}%")
#         goldPityCount = 0
#         goldCount += 1
#     elif result <= 13:
#         print(f"{purple} Pull {counter + 1}: 4**** Purple - {result}%")
#         purplePityCount = 0
#         goldPityCount += 1
#         purpleCount += 1
#     else:
#         print(f"{blue} Pull {counter + 1}: 3*** Blue - {result}%")
#         goldPityCount += 1
#         purplePityCount += 1
#         blueCount += 1
#
#     counter += 1
# print(f"\n{white}Total number of pulls: {pullCount}")
# print(f"\nGacha results:\n{gold}5***** Gold count: {goldCount}\n{purple}4**** Purple count: {purpleCount}\n{blue}3*** Blue count: {blueCount}\n")
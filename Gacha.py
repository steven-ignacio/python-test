import random
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    try:
        message = "Hello World!!"
        return render_template('index.html', message = message)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/result', methods=['POST'])
def result():
    # iterator
    counter = 0

    # pity counters
    goldPityCount = 0
    purplePityCount = 0
    softPityRate = 0

    # pull counters
    goldCount = 0
    purpleCount = 0
    blueCount = 0
    displayResult = ""

    pullCount = int(request.form['number'])

    while counter < pullCount:
        result = round(float(random.random() * 100), 2)

        if counter % 10 == 0:  # adds a line break every 10 pulls
            displayResult += f"\n<p>Multi-pull #{counter // 10 + 1}</p>"

        # guarantees the next pull if pity is hit
        if purplePityCount == 9: result = 13
        if goldPityCount == 89: result = 1.6

        # roll logic
        if goldPityCount >= 74:
            softPityRate = (goldPityCount - 73) * 0.6

        if result <= 1.6 + softPityRate:
            displayResult += f"<p class='gold'> Pull {counter + 1}: 5***** Gold!!! - {result}%</p>"
            goldCount += 1
            softPityRate = 0
            goldPityCount = 0
        elif result <= 13:
            displayResult += f"<p class='purple'> Pull {counter + 1}: 4**** Purple - {result}%</p>"
            purplePityCount = 0
            goldPityCount += 1
            purpleCount += 1
        else:
            displayResult += f"<p class='blue'> Pull {counter + 1}: 3*** Blue - {result}%</p>"
            goldPityCount += 1
            purplePityCount += 1
            blueCount += 1

        counter += 1
    displayResult += f"\n<p>Total number of pulls: {pullCount}</p>"
    displayResult += f"\nGacha results:\n<p class='gold'>5***** Gold count: {goldCount}</p>\n<p class='purple'>4**** Purple count: {purpleCount}</p></p>\n<p class='blue'>3*** Blue count: {blueCount}</p>\n"

    return render_template('result.html', displayResult = displayResult, pullCount = pullCount)

if __name__ == "__main__":
    app.run()

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
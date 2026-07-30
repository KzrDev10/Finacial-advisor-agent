def assess_risk_profile(age,timeline_year,volatility_comfort):
    points = 0

    #age point classification
    if age < 30:
        points += 3
    elif age>29 and age<=50:
        points += 2
    elif age > 50:
        points+=1

    #timeline point classification
    if timeline_year > 10:
        points += 3
    elif timeline_year >= 4 and timeline_year<= 10:
        points += 2
    elif timeline_year >0 and timeline_year <=3:
        points+=1
    
    # volatility point classification
    if volatility_comfort >= 7 and volatility_comfort <=10:
        points+=3
    elif volatility_comfort >= 4 and volatility_comfort <=6:
        points+=2
    elif volatility_comfort >= 1 and volatility_comfort <=3:
        points += 1


    if points <= 4:
        return "Conservative"
    elif points == 5 or points == 6:
        return "Moderate"
    elif points >= 7:
        return "Aggressive"

    
       
if "__main__" == __name__:
    print(assess_risk_profile(40,4,1))
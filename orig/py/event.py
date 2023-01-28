from evaluate_event import EvaluateEvent


#Qui importo tutto quanto l'oggetto
evaluateEvent = EvaluateEvent()

#Qui calcolo la probabilità che sia in acqua oppure no
# Qui viene usato il file data/underwater/percent_prob_underwater.hdr
a, b = evaluateEvent.percentProbIsUnderwater(-0.01, 123.17, 10, 13, 178)
print(a, b)
from openskill import Rating, rate, ordinal
from openskill.models import BradleyTerryFull
import json
import sys

trainerFile = open("data/trainers.json", "r", encoding="utf-8")
trainers = json.load(trainerFile)
trainerFile.close


matchesFile = open(sys.argv[1], "r", encoding="utf-8")
matches = json.load(matchesFile)

for match in matches["matches"]:
    participants = []
    oldRankings = []
    newRankings = []
    ranks = []
    for participant in match:
        participants.append(participant)
        oldRankings.append([Rating(mu=trainers[participant].pop("mu"), sigma=trainers[participant].pop("sigma"))])
        ranks.append([match[participant]]) 
    newRankings = rate(oldRankings, rank=ranks)
    for idx, x in enumerate(participants):
        trainers[x].pop("ordinal")
        trainers[x]["mu"] = newRankings[idx][0].mu
        trainers[x]["sigma"] = newRankings[idx][0].sigma
        trainers[x]["ordinal"] = ordinal([newRankings[idx][0].mu, newRankings[idx][0].sigma])
trainerFile = open("data/trainers.json", "w", encoding="utf-8")
json.dump(trainers, trainerFile, sort_keys=True, indent=4)
trainerRanking = {}
for trainer in trainers:
    trainerRanking[trainers[trainer]["name"]] = trainers[trainer]["ordinal"]
trainerRankingSortedKeys = sorted(trainerRanking, key=trainerRanking.get, reverse=True)
for r in trainerRankingSortedKeys:
    print(r, trainerRanking[r])
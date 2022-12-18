from openskill import Rating, rate, ordinal
from openskill.models import BradleyTerryFull
import json

trainerFile = open("data/trainers.json", "r", encoding="utf-8")
trainers = json.load(trainerFile)
trainerFile.close
# trainerFile = open("data/trainers.json", "w", encoding="utf-8")


matchesFile = open("data/matches/trainerBattle/leaderTournament/unityVillage2022-07/results.json", "r", encoding="utf-8")
matches = json.load(matchesFile)

for match in matches["matches"]:
    trainer1 = list(match.keys())[0]
    trainer2 = list(match.keys())[1]
    print(trainers[trainer1]["name"] + " vs " + trainers[trainer2]["name"])
    trainer1OldRating = Rating(mu=trainers[trainer1].pop("mu"), sigma=trainers[trainer1].pop("sigma"))
    trainer2OldRating = Rating(mu=trainers[trainer2].pop("mu"), sigma=trainers[trainer2].pop("sigma"))
    result = [[trainer1NewRating], [trainer2NewRating]] = rate([[trainer1OldRating], [trainer2OldRating],], rank=[match[trainer1], match[trainer2]])
    trainers[trainer1].pop("ordinal")
    trainers[trainer2].pop("ordinal")
    trainers[trainer1]["mu"] = trainer1NewRating.mu
    trainers[trainer1]["sigma"] = trainer1NewRating.sigma
    trainers[trainer2]["mu"] = trainer2NewRating.mu
    trainers[trainer2]["sigma"] = trainer2NewRating.sigma
    trainers[trainer1]["ordinal"] = ordinal([trainer1NewRating.mu, trainer1NewRating.sigma])
    trainers[trainer2]["ordinal"] = ordinal([trainer2NewRating.mu, trainer2NewRating.sigma])
# json.dump(trainers, trainerFile, sort_keys=True, indent=4)
trainerRanking = {}
for trainer in trainers:
    trainerRanking[trainer["name"]] = trainer["ordinal"]
trainerRankingSortedKeys = sorted(trainerRanking, key=trainerRanking.get, reverse=True)
for r in trainerRankingSortedKeys:
    print(r, trainerRanking[r])
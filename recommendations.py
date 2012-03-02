critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0, 
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener':4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane':4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5
    },
    'Toby': {
        'Snakes on a Plane': 4.5,
        'You, Me and Dupree': 1.0,
        'Superman Returns': 4.0
    }
}


from math import sqrt

def sim_distance(prefs, person1, person2):
    flag = False
    sum_of_squares = 0

    for item in prefs[person1]:
        if item in prefs[person2]:
            flag = True
            sum_of_squares += pow(prefs[person1][item] - prefs[person2][item], 2)

    if not flag:
        return 0

    return 1/(1+sqrt(sum_of_squares))

def sim_tanimoto_distance(prefs, p1, p2):
    ma, mb, ab = 0, 0, 0
    for item, rating1 in prefs[p1].iteritems():
        for item2, rating2 in prefs[p2].iteritems():
            if item != item2:
                continue
            ab += rating1 * rating2
            ma += rating1 ** 2
            mb += rating2 ** 2

    if ma + mb == 0:
        return 0

    return ab / (ma + mb - ab)

def sim_pearson(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    n = len(si)
    if n == 0:
        return 1

    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    num = pSum - sum1 * sum2 / n
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0

    r = num / den
    return r

def sim_people(sim):
    people = critics.keys()
    fmt = [ -len(p)-3 for p in people ]
    col0 = min(fmt)
    fmt.insert(0, col0)

    def mold(text, width, type_='s'):
        fmt = '%'+str(width)+type_
        print fmt % text,

    for i, title in enumerate([' ']+people):
        mold(title, fmt[i])
    print

    for i, p1 in enumerate(people):    
        mold(p1, fmt[0])
        for j, p2 in enumerate(people):
            if i <= j:
                mold(sim(critics, p1, p2), fmt[j+1], '.2g')
            else:
                mold('', fmt[j+1])
        print

def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    scores.sort(reverse=True)
    return scores[:n]

def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        if other == person: continue
        sim = similarity(prefs, person, other)

        if sim <=0: continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim

                simSums.setdefault(item, 0)
                simSums[item] += sim

    rankings = [(total/simSums[item], item) for item, total in totals.items()]
    rankings.sort(reverse=True)
    return rankings

def getRecommendations2(prefs, peopleMatch, user):
    has_rated = set(prefs[user].keys())

    totals = {}
    simSums = {}
    for sim, person in peopleMatch[user]:
        for item, rating in prefs[person].items():
            if item in has_rated:
                continue
            totals.setdefault(item, 0)
            totals[item] += sim * rating

            simSums.setdefault(item, 0)
            simSums[item] += sim

    rankings = [ (total/simSums[item], item) for item, total in totals.items() ]
    rankings.sort(reverse=True)
    return rankings

def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]
    return result

def calculateSimilarItems(prefs, n=10):
    result = {}

    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        c += 1
        if c % 100 == 0:
            print "%d / %d" % (c, len(itemPrefs))
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result

def calculateSimilarPeople(prefs, n=5):
    return dict([(p, topMatches(prefs, p, n=n, similarity=sim_pearson))
        for p in prefs])

def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    for item, rating in userRatings.items():
        for similarity, item2 in itemMatch[item]:
            if item2 in userRatings: continue
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    rankings = [(score/totalSim[item], item) for item,score in scores.items()]
    rankings.sort(reverse=True)
    return rankings

    


if __name__ == '__main__':
    sim_people(sim_pearson)
    sim_people(sim_distance)
    sim_people(sim_tanimoto_distance)

    print '#1'
    print getRecommendations(critics, 'Toby')
    peopleim = calculateSimilarPeople(critics)
    print getRecommendations2(critics, peopleim, 'Toby')
    print getRecommendations(critics, 'Toby', sim_distance)
    print getRecommendations(critics, 'Toby', sim_tanimoto_distance)
    print '-'*10

    movies = transformPrefs(critics)
    print topMatches(movies, 'Superman Returns')
    print topMatches(movies, 'Superman Returns', similarity=sim_distance)
    print topMatches(movies, 'Superman Returns', similarity=sim_tanimoto_distance)
    print '-'*10

    print getRecommendations(movies, 'Just My Luck')
    print '-'*10

    itemsim = calculateSimilarItems(critics)
    print getRecommendedItems(critics, itemsim, 'Toby')


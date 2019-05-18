import sys, random

random.seed(10000) # Use this seed (10000) when submitting to autolab

class BayesNet:
    """
    variables: dictionary mapping letter (ex: 'A') to a Variable object
    letters: list of letters in topological order
    query: Query object representing the query variable and evidence variables
    """
    def __init__(self, filepath):
        self.variables = {}
        self.letters = []
        self.query = None

        with open(filepath) as reader:
            self.letters = reader.readline().rstrip().split(' ')
            for letter in self.letters:
                self.variables[letter] = Variable(letter)

            # Read conditional probabilities until we hit an empty line
            for line in iter(reader.readline, '\n'):
                components = line.rstrip().split(' ')
                self.process_components(components)

            # Finally, read the query
            line = reader.readline()
            query_components = line.rstrip().split(' ')
            dep_var = query_components.pop(0)
            self.query = Query(dep_var, query_components)

    def process_components(self, components):
        """
        Updates Bayes Net probabilities and structure. 
        components : list describing a conditional probability from the Bayes Net
                     (ex: ['+A', '-B', 'C', '0.5'] -> P(+C | +A, -A) = 0.5)

        """
        probability = float(components.pop())
        dep_var = components.pop()
        parents = [s[1] for s in components]
        values = tuple((s[0]=="+") for s in components)
        
        if (len(parents) > 0):
            self.variables[dep_var].parents = parents
            self.add_children(dep_var, parents)
            self.variables[dep_var].distribution[values] = probability
        else:
            self.variables[dep_var].probability = probability
    
    def add_children(self, dep_var, parents):
        """
        Add dep_var to the children list of each parent
        """
        for parent in parents:
            if dep_var not in self.variables[parent].children:
                self.variables[parent].children.append(dep_var)

    def sample(self, probability):
        """
        Use this function when generating random assignments.
        You should not be generating random numbers elsewhere.
        """
        return random.uniform(0, 1) < probability

    def direct_sample(self, trials):
        """
        Example of a direct sampling impementation. Ignores evidence variables.
        You do not need to edit this.
        """
        count = 0
        for i in xrange(trials):
            values = {}
            for letter in self.letters:
                prob = self.variables[letter].get_prob(values)
                values[letter] = self.sample(prob)
            if values[self.query.variable]:
                count += 1
        return float(count) / trials

    def rejection_sample(self, trials):
        count = 0
        total = 0
        for i in xrange(trials):
            values = {}
            for letter in self.letters:
                prob = self.variables[letter].get_prob(values)
                values[letter] = self.sample(prob)
            allRight = True
            for j in self.query.evidence.keys():
                if (self.query.evidence[j] != values[j]):
                    allRight = False
            if allRight:
                total += 1
                if values[self.query.variable]:
                    count += 1
        return float(count) / total

    def likelihood_sample(self, trials):
        """
        Implement this!
        Returns the estimated probability of the query.
        """
        weightsDict = {}
        count = 0.0
        total = 0.0
        evidenceKeys = self.query.evidence.keys()
        
        for i in xrange(trials):
            values = {}
            weight = 1.0
            temp = []
            
            for letter in self.letters:
                if not (letter in evidenceKeys):
                    prob = self.variables[letter].get_prob(values)
                    values[letter] = self.sample(prob)
                else:
                    pr = self.variables[letter].get_prob(values)
                    weight = weight * pr
                    values[letter] = self.query.evidence[letter]
                
                temp.append(values[letter])
            temp = tuple(temp)
            
            if (temp in weightsDict):
                weightsDict[temp] = weightsDict[temp] + weight
            else:
                weightsDict[temp] = weight
        
        ind = self.letters.index(self.query.variable)
        for vals in weightsDict:
            if vals[ind]:
                count += weightsDict[vals]
            total += weightsDict[vals]
                
        if len(evidenceKeys) == 0:
            return count / trials
        else:
            return 2.0 * (count / trials)

    def gibbs_sample(self, trials):
        return 1.0

class Variable:
    """
    letter: the letter (ex: 'A')
    distribution: dictionary mapping ordered values of parents to float probabilities,
                  ex: (True, True, False) -> 0.5
    parents: list of parents (ex: ['C', 'D'])
    children: list of children (ex: ['E'])
    probability: probability of node if the node has no parents
    """
    def __init__(self, letter):
        self.letter = letter
        self.distribution = {} # Maps values of parents (ex: True, True, False) to
        self.parents = []
        self.children = []
        self.probability = 0.0 # Only for variables with no parents

    def get_prob(self, values):
        if len(self.parents) == 0:
            return self.probability
        else:
            key = tuple([values[letter] for letter in self.parents])
            return self.distribution[key]

class Query:
    """
    self.variable: the dependent variable associated with the query
    self.evidence: mapping from evidence variables to True or False
    """
    def __init__(self, variable, evidence):
        self.variable = variable
        self.evidence = {}
        for s in evidence: # ex: "+B" or "-C"
            self.evidence[s[1]] = (s[0] == "+")

if __name__ == '__main__':
    filename = sys.argv[1]
    trials = int(sys.argv[2])
    sampling_type = int(sys.argv[3])
    bayes_net = BayesNet(filename)

    if sampling_type == 0:
        print bayes_net.direct_sample(trials)
    elif sampling_type == 1:
        print bayes_net.rejection_sample(trials)
    elif sampling_type == 2:
        print bayes_net.likelihood_sample(trials)
    elif sampling_type == 3:
        print bayes_net.gibbs_sample(trials)
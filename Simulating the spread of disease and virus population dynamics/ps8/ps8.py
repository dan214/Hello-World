



import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """


        SimpleVirus.__init__(self,maxBirthProb, clearProb)
        
        self.resistances= resistances
        self.mutProb= mutProb



    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        return (self.resistances[drug])


    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        count = 0
        for i in activeDrugs:
            if self.isResistantTo(i) == True:
                count += 1
            else:
                raise NoChildException
        if (count >= 0):
            newResistances = {}
            if random.random() <= (self.maxBirthProb * (1 - popDensity)):
                for i in self.resistances:
                    if random.random() <= self.mutProb:
                        newResistances[i] = not self.isResistantTo(i)
                    else:
                        newResistances[i] = self.isResistantTo(i)
                    
                        

            #print "new Resistances ",newResistances
            
                childVirus = ResistantVirus(self.maxBirthProb,self.clearProb,newResistances,self.mutProb)
                return childVirus
            else:
                raise NoChildException()
            
            

            

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        #SimplePatient.__init__(self,viruses,maxPop)
        self.viruses = viruses
        self.maxPop = maxPop
        self.drugs = []
    

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        if (newDrug) in self.drugs:
            print "Drug already being administered"
        else:
            self.drugs.append(newDrug)
        


    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.drugs
        

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        virusResist = 0
        for i in (self.viruses):
            count = 0
            for x in drugResist:
                if i.isResistantTo(x) == False:
                    count += 1
            if count == 0:
                virusResist += 1

        return virusResist
    
                    
                   


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        self.UpdatedViruses = []
        for i in self.viruses:
            if((i.doesClear()) == False):
                self.UpdatedViruses.append(i)

        self.viruses = self.UpdatedViruses
            
        popDensity = float(len(self.UpdatedViruses)/self.maxPop)

        for x in self.viruses:
            try:
                self.UpdatedViruses.append(x.reproduce(popDensity,self.drugs))
            except NoChildException:
                pass
        self.viruses = self.UpdatedViruses
        return len(self.viruses)
       




#
# PROBLEM 2
#

def simulationWithDrug():

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    viruses = []
    #list of SimpleVirus instances
    numberOfViruses = 100 #the number of SimpleVirus instances
    resistances = {'guttagonol':False,'grimpex':False}
    for i in range(numberOfViruses):
        #instantiate each virus and append it to our list

            i = ResistantVirus(0.1,0.05,resistances,0.005)
            
            viruses.append(i)
    firstPatient = Patient(viruses,1000)
   
    
    virusPop = []
    timeSteps = []
    averageViruses = []
    averageResistantViruses = []
    averageResistant2Viruses = []
    reps = 1
    resistPop = []
    aresistPop = []
    firstSteps = 150
    finalSteps = 150
    for i in range(reps):

        
        
        for i in range(450):
            resistPop.append(0)
            averageViruses.append(0)
            averageResistantViruses.append(0)
            averageResistant2Viruses.append(0)
            virusPop.append(0)
            timeSteps.append(i)
            aresistPop.append(0)
            
        for i in range(150):
            
            virusPop[i] += firstPatient.update()
            resistPop[i] += firstPatient.getResistPop(['guttagonol'])
            aresistPop[i] += firstPatient.getResistPop(['grimpex'])
            
            
        firstPatient.addPrescription('guttagonol')
        for x in range(firstSteps,(finalSteps + 150)):
            virusPop[x] += firstPatient.update()
            resistPop[x] += firstPatient.getResistPop(['guttagonol'])
            aresistPop[x] += firstPatient.getResistPop(['grimpex'])
            
        firstPatient.addPrescription('grimpex')
        for y in range(finalSteps + 150,(finalSteps * 3)):
            virusPop[y] += firstPatient.update()
            resistPop[y] += firstPatient.getResistPop(['guttagonol'])
            aresistPop[y] += firstPatient.getResistPop(['grimpex'])
            
    for time in range((firstSteps * 3)):
        averageViruses[time] = float(virusPop[time])/reps
        averageResistantViruses[time] = float(resistPop[time])/reps
        averageResistant2Viruses[time] = float(resistPop[time])/reps
    
    print virusPop
    print resistPop
    print aresistPop
    pylab.plot(timeSteps,virusPop)
    pylab.plot(timeSteps,resistPop)
    pylab.plot(timeSteps,aresistPop)
    pylab.xlabel("Number of elasped time steps")
    pylab.ylabel("The population of the resistant virus in the patient")
    pylab.show()

   

        
    
    



#
# PROBLEM 3
#        

def simulationDelayedTreatment():

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """

    viruses = []
    #list of SimpleVirus instances
    numberOfViruses = 100 #the number of SimpleVirus instances
    resistances = {'guttagonol':False,'grimpex':False}
    
    
    firstPatient = Patient(viruses,1000)
    for i in range(numberOfViruses):
        #instantiate each virus and append it to our list

            i = ResistantVirus(0.1,0.05,resistances,0.005)
            
            viruses.append(i)
   
    
    virusPop = []
    timeSteps = []
    averageViruses = []
    averageResistantViruses = []
    x = 300
    resistPop = []
    firstSteps = 150
    finalSteps = 150
        

    for i in range(x + 150):
        resistPop.append(0)
        averageViruses.append(0)
        averageResistantViruses.append(0)
        virusPop.append(0)
        timeSteps.append(i)
    for y in range(x):
            
            virusPop[y] += firstPatient.update()
            resistPop[y] += firstPatient.getResistPop(['guttagonol'])
    firstPatient.addPrescription('guttagonol')

    for z in range(x,(x + 150)):
            
            virusPop[z] += firstPatient.update()
            resistPop[z] += firstPatient.getResistPop(['guttagonol'])

    print virusPop
    print resistPop
    pylab.plot(timeSteps,virusPop)
    pylab.plot(timeSteps,resistPop)
    pylab.xlabel("Number of elasped time steps")
    pylab.ylabel("The population of the resistant virus in the patient")
    
    pylab.figure()

    pylab.show()
#simulationDelayedTreatment()
simulationWithDrug()
#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    # TODO



#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations():

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    #TODO




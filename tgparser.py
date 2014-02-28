#============================================================================
#                           PRAAT Text Grid File Parser
#============================================================================
# Script name: tgparser.py
# Created on: 21/02/2014
# Author: Paula D. Paro Costa
# Purpose: API to parse and get relevant information from a Praat annotation
#          file. For more information, refer to:
#          http://www.fon.hum.uva.nl/praat/manual/TextGrid.html
#
# Notice:
# Copyright (C) 2013  Paula D. Paro Costa
#
#    tgparser.py is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    tgparser.py is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You can access a copy of the GNU General Public License at
#    <http://www.gnu.org/licenses/>.
#=============================================================================



import re
import numpy as np

class parseTG:
    
    def __process_point(self,tgfile):
        '''
        Process Point 
        points [x]:
        number = 0.49363748331322405 
        mark = "\ep"

        '''
        line=tgfile.readline()
        token='points \['
        if re.search(token,line)==None:
            print 'Error to process point.'
            status=-1
        else:
            line=tgfile.readline()
            token='number'
            point=self.__process_numeric(token,line)
            if point==None:
                print 'Error to process point.'
                status=-1
            else:
                line=tgfile.readline()
                token='mark'
                mark=self.__process_text(token,line)
                if mark==None:
                    print 'Error to process interval name.'
                    status=-1
                else:
                    status=0
                    print str(point)+'\t'+mark
                    return status, point, mark

    def __process_numeric(self,token,line):
        """
        Process a numeric field.

        The expected line is:
        <token> = <float> \n"

        Returns <float> or None.
        """
        result=re.search(token+' = ',line)
        if result!=None:
            tail=line[result.end():]
            result=re.search(' \n',tail)
            return float(tail[:result.start()])
        return result

    def __process_text(self,token,line):
        """
        Process a text token.
        The expected line is:
        <token> = "<text>" \n
        Returns <text> or None.
        """
        result=re.search(token+' = \"',line);
        if result!=None:
            tail=line[result.end():]
            result=re.search('\" \n',tail)
            return tail[:result.start()]
        return result

    def __process_interval(self,tgfile):
        """
        Process an interval.
            
        intervals [x]:
        xmin = 0
        xmax = 13.664
        text = ""

        """
        
        line=tgfile.readline()
        token='intervals \['
        if re.search(token,line)==None:
            print 'Error to process interval.'
            status=-1
        else:
            line=tgfile.readline()
            token='xmin'
            boundary=self.__process_numeric(token,line)
            if boundary==None:
                print 'Error to process boundary.'
                status=-1
            else:
                line=tgfile.readline()
                token='xmax'
                if re.search(token,line)==None:
                    print 'Error to process interval.'
                    status=-1
                else:
                    line=tgfile.readline()
                    token='text'
                    interval_name=self.__process_text(token,line)
                    if interval_name==None:
                        print 'Error to process interval name.'
                        status=-1
                    else:
                        status=0
                        print str(boundary)+'\t'+interval_name
        return status, boundary, interval_name
    

    def __process_tier(self,tgfile,boundaries,labels,tierstamps):
        
        line=tgfile.readline()
        token='item \['
        if re.search(token,line)==None:
            print 'Error to process tier, while retrieving: '+token+' .'
            status=-1
        else:
            line=tgfile.readline()
            token='class'
            tier_class=self.__process_text(token,line)
            if tier_class==None:
                print 'Error to process tier, while retrieving: '+token+' .'
                status=-1
            elif tier_class=="IntervalTier":
                line=tgfile.readline()
                token='name'
                tier_name=self.__process_text(token,line)
                if tier_name==None:
                    print 'Error to process tier, while retrieving: '+token+' .'
                    status=-1
                else:
                    line=tgfile.readline()
                    token='xmin'
                    if re.search(token,line)==None:
                        print 'Error to process tier, while retrieving: '+token+' .'
                        status=-1
                    else:
                        line=tgfile.readline()
                        token='xmax'
                        tier_xmax=self.__process_numeric(token,line)
                        if tier_xmax==None:
                            print 'Error to process tier, while retrieving: '+token+' .'
                            status=-1
                        else:
                            line=tgfile.readline()
                            token='intervals: size'
                            number_of_intervals=self.__process_numeric(token,line)
                            print 'Processing '+str(int(number_of_intervals))+' intervals...'
                            if number_of_intervals==None:
                                print 'Error to process tier, while retrieving: '+token+' .'
                                status=-1
                            else:
                                for i in range(int(number_of_intervals)):
                                    status, new_boundary, interval_name=self.__process_interval(tgfile)
                                    if status!=-1:
                                        boundaries.append(new_boundary)
                                        labels.append(interval_name)
                                        tierstamps.append(tier_name)
                                        status=0
                            
            elif tier_class=="TextTier":
                
                line=tgfile.readline()
                token='name'
                tier_name=self.__process_text(token,line)
                
                if tier_name==None:
                    print 'Error to process tier, while retrieving: '+token+' .'
                    status=-1
                else:
                    line=tgfile.readline()
                    token='xmin'
                    if re.search(token,line)==None:
                        print 'Error to process tier, while retrieving: '+token+' .'
                        status=-1
                    else:
                        line=tgfile.readline()
                        token='xmax'
                        tier_xmax=self.__process_numeric(token,line)
                        if tier_xmax==None:
                            print 'Error to process tier, while retrieving: '+token+' .'
                            status=-1
                        else:
                            line=tgfile.readline()
                            token='points: size'
                            number_of_points=self.__process_numeric(token,line)
                            print 'Processing '+str(int(number_of_points))+' intervals...'
                            if number_of_points==None:
                                print 'Error to process tier, while retrieving: '+token+' .'
                                status=-1
                            else:
                                for i in range(int(number_of_points)):
                                    status, new_point, mark_name=self.__process_point(tgfile)
                                    if status!=-1:
                                        boundaries.append(new_point)
                                        labels.append(mark_name)
                                        tierstamps.append(tier_name)
                                        status=0
            
        return status, boundaries, labels, tierstamps, tier_name, tier_class, tier_xmax

        
        

    def __parseTextGrid(self,TextGridFile):
        '''
        Parses a TextGrid file.

        Key arguments:
        TextGridFile - path to TextGrid file

        Outputs:
        status - '0' if Ok, '-1' if something went bad during parsing
        tgxmin - xmin of TextGrid file
        tgxmax - xmax of TextGrid file
        boundaries - list of all boundaries of all tiers in the file, to be indexed by 'labels' and 'tierstamps' lists
        tierstamps - tier names associated to each boundary listed in 'boundaries'
        classes - classes of all the tiers in the TextGrid
        tierorder - tiers in the same sequence they appear in the file
        xmax - list of xmax for all tiers
        
        '''
        status=0
        i=0
        boundaries=[]
        labels=[]
        tierstamps=[]
        classes=dict()
        xmax=dict()
        tgfile=open(TextGridFile)
        line=tgfile.readline()
        tierorder=[]
        print line
        token='File type'
        if re.search(token,line)==None:
            print 'Error while retrieving: '+token+'. The file seems to be invalid.'
        else:
            line=tgfile.readline()
            print line
            token='Object class'
            if re.search(token,line)==None:
                print 'Error while retrieving: '+token+'. The file seems to be invalid.'
            else:
                line=tgfile.readline() # Discard blank line
                print line
                line=tgfile.readline()
                print line
                token='xmin'
                tgxmin=self.__process_numeric(token,line)
                if tgxmin==None:
                    print 'Error while retrieving: '+token+'. The file seems to be invalid.'
                else:
                    line=tgfile.readline()
                    print line
                    token='xmax'
                    tgxmax=self.__process_numeric(token,line)
                    if tgxmax==None:
                        print 'Error while retrieving: '+token+'. The file seems to be invalid.'
                    else:
                        line=tgfile.readline()
                        print line
                        token='tiers\? <exists>'
                        if re.search(token,line)==None:
                            print 'The file does not have any tiers to process... Bye!'
                        else:
                            line=tgfile.readline()
                            print line
                            token='size'
                            number_of_tiers=self.__process_numeric(token,line)
                            if number_of_tiers==None:
                                print 'Error while retrieving: '+token+'. The file seems to be invalid.'
                            else:
                                line=tgfile.readline()
                                token='item \[\]'
                                if re.search(token,line)==None:
                                    print 'Error while retrieving: '+token+'. The file seems to be invalid.'
                                else:
                                    for i in range(int(number_of_tiers)):
                                        
                                        status,boundaries,labels,tierstamps,tier_name,tier_class,tier_xmax=self.__process_tier(tgfile,boundaries,labels,tierstamps)
                                                                                                               
                                        if status==-1:
                                            print 'Error while processing tier number '+(i+1)+'. Bye!'
                                            break
                                        print 'Tier \"'+tier_name+'/" processed with sucess.'
                                        tierorder.append(tier_name)
                                        classes.update({tier_name:tier_class})
                                        xmax.update({tier_name:tier_xmax})
                                        
        return status, tgxmin,tgxmax,boundaries, labels, tierstamps, classes, tierorder, xmax
    

    def __init__(self,tgfile):

        self.status=-1
        self.__boundaries=[]
        self.__labels=[]
        self.__tierstamps=[]
        self.__classes=dict()
        self.__xmax=dict()
        self.tgxmin=0
        self.tgxmax=0


        self.status, self.tgxmin, self.tgxmax, self.__boundaries, self.__labels, self.__tierstamps, self.__classes,tierorder,self.__xmax=self.__parseTextGrid(tgfile)
        self.__boundaries=np.asarray(self.__boundaries)
        self.__labels=np.asarray(self.__labels)
        self.__tierstamps=np.asarray(self.__tierstamps)
        self.tiers=tierorder

        if self.status==-1:
            print "Failed to parse TextGrid file: "+tgfile

    def printTiersInfo(self):
        '''

        Print the list of the tiers in the TextGrid file and their classes.

        '''
        
        for i in self.tiers:
            print i+": "+self.__classes[i]
        return
          

    def getTierAnnotation(self,tiername):
        '''

        Returns a list of labels and their boundaries for a given tier.
        If the tier is an "IntervalTier", it is composed of a sequence of intervals and the boundary
        associated to a label informs the beginning of the interval (the
        beginning of the following interval is the ending of the current interval).
        It the tier is a "PointTier" the boundary simply informs the label instant.

        Key argument:
        tiername - tier name to be processed

        '''

        ind=np.where(self.__tierstamps==tiername)[0]
        if len(ind)!=0:
            labels=self.__labels[ind]
            boundaries=self.__boundaries[ind]
        else:
            print "Invalid tier name: "+tiername
            labels=None
            boundaries=None
        return labels, boundaries
   

    def getTierXmax(self,tiername):
        '''

        Returns xmax for a given tier.
        
        Key argument:
        tiername - tier name to be processed
        '''

        try:
            return self.__xmax[tiername]
        except KeyError:
            print "Key error. Invalid tier name: "+tiername
            return None
         

    def getTierClass(self,tiername):
        '''
        Returns the class of a given tier.

        Key argument:
        tiername - tier name to be checked.

        '''
        try:
            return self.__classes[tiername]
        except KeyError:
            print "Key error. Invalid tier name: "+tiername
            return None
        
    def labelSummary(self,labeltofind,tiername):
        '''
        Given a label and a tier to be analyzed, the function returns a summary
        of this label in the tier, informing their boundaries, number of occurrences, and durations.

        Key arguments:
        labeltofind - Label string to be searched (it should be identical to the one recorded in Praat).
        tiername - tier name to be analyzed.
        
        '''
        
        labels,boundaries=self.getTierAnnotation(tiername)
        if labels==None or boundaries==None:
            boundaries=None
        ind=np.where(labels==labeltofind)[0]
        if len(ind)!=0:
            foundat=boundaries[ind]
            occurrences=len(ind)
            durations=np.zeros(len(ind))
            for i in range(len(ind)):
                if ind[i]+1>=len(boundaries):
                    d=self.__xmax[tiername]-boundaries[ind[i]]
                else:
                    d=boundaries[ind[i]+1]-boundaries[ind[i]]
                durations[i]=d
        else:
            print "Label not found in this tier."
            foundat=None
            occurrences=0
            durations=None

        return foundat,occurrences,durations

    def getFirstLB(self,tiername):
        '''
        Informs the first label and boundary of a given tier.

        Key arguments:
        tiername - tier to be analyzed.

        '''
        
        labels,boundaries=self.getTierAnnotation(tiername)
        if labels==None or boundaries==None:
            firstl=labels
            firstb=boundaries
        firstl=labels[0]
        firstb=boundaries[0]
        return firstl, firstb

    def getLastLB(self,tiername):
        '''
        Informs the last label and boundary of a given tier.

        Key arguments:
        tiername - tier to be analyzed.

        '''
  
        labels,boundaries=self.getTierAnnotation(tiername)
        if labels==None or boundaries==None:
            lastl=labels
            lastb=boundaries
        lastl=labels[-1]
        lastb=boundaries[-1]
        return lastl,lastb    

                

                
                

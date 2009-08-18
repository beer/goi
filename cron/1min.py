#!/usr/bin/python2.5
from time import time
import goi

now = datetime.fromtimestamp(int(time()))
finishes = goi.Task.gql('WHERE et <= :1', now)


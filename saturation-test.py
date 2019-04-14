#!/usr/bin/env python 
import math

cols = (255,10,50)

def colorsqrt(cols):
	return math.sqrt(
		(cols[0]*cols[0]) +
		(cols[1]*cols[1]) +
		(cols[2]*cols[2])
	)

def sattest(cols, change):
	p = colorsqrt(cols)

	R=p+((cols[0])-p)*change
	G=p+((cols[1])-p)*change
	B=p+((cols[2])-p)*change

	return (R,G,B)

def norms(cols):
	mins = min(cols[0], cols[1], cols[2])
	if mins < 0:
		cols = (cols[0]+(-1*mins), cols[1]+(-1*mins), cols[2]+(-1*mins))

	print cols
	sums = (cols[0]) + (cols[1]) + (cols[2])
	r = cols[0]/sums*255
	g = cols[1]/sums*255
	b = cols[2]/sums*255
	
	return(r,g,b)



def brightness(cols, change):
    if change <= 0:
        change = (change*-1)+0000.1

    if change >= 1:
        change = 1/change

    # there should be a per color difference in the change since humans eyes and brains, it shall be later.

    return cols[0]*change, cols[1]*change, cols[2]*change

result = sattest(cols, 2)
print(result)
result = norms(result)
print(result)
result = brightness(result, 0.95)
print(result)


# AI_Rat_Saper
This is student project of AI rat saper defusing bomb on randomly generated field with use of decision tree, genetic algorith, a* algorithm and image recognition with neural networks.

How it works:
1. Field is randomly generated in matrix where:
	- T - terrain
	- B - bomb
	- R - rock
	- P - puddle
2. Rat can not move through rocks, going through puddles is slower than normal terrain
3. Genetic algorithm finding the shortest way to move through all bomb squares
4. A* algorithm finding best way from one bomb square to another with respect of those rules:
	- Rat can go through terrain and bomb squares normally
	- Rat moving through puddles slower than through terrain and bomb squares
	- Rat can not move through rocks
5. When on bomb square, rat judges with image recognition whether its a rock or a mine (if rock, then field changing icon to rock)
6. If its a mine, rat judges what to do with it basing on decision tree:
	- Take away to sapper grounds (field changing icon to red flag)
	- Defuse here (field changing icon to crossed mine)
7. Program ends when rat will cover all bomb squares


Presentation:


https://github.com/adbreeker/AI_Rat_Saper/assets/111668308/5a2b8c47-df79-4c5b-ab37-ac1d0cfd5375


a:
	git add .
	git commit -m "this commit is only to sync the code on 2 different machines"
	git push

b: 
	rm ./resources/tmp/age.tmp

c:
	rm ./resources/tmp/blocks/blocks.data

d:
	python peer.py
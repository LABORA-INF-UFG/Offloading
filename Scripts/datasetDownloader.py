import gdown

def main ():

	id = "17yMsaR_MGhUaEgoUBn5P3_50qqarr7lP"
	gdown.download(id=id, output='offloadingPaperPIMRC2023dataset.zip', quiet=False)

if __name__ == '__main__':
	main()
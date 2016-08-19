import argparse
import re
import ArpaLM

def tokenize(filename):	
	file = open(filename).read()
	sentences = re.split('!?.\n', file)
	return [s.split(" ") for s in sentences]


def create_alg(alg, sentences=None):
	if not alg:
		return None

	if alg == "LBL":
		import lbl
		return lbl.LBL(sentences)
	if alg == "HLBL":
		import hlbl
		return hlbl.HLBL(sentences)
	if alg == "LBL_MP":
		import lbl_mp
		return lbl_mp.LBL(sentences)


def train(alg, filename, save_net):
	sentences = tokenize(filename)
	lm = create_alg(alg, sentences)
	if save_net:
		lm.save(save_net)


def evaluate(alg, filename, net, arpa=None, weight=0):
	sentences = tokenize(filename)
	lm = create_alg(alg)
	lm.load(net)

	lm.perplexity(sentences, arpa, weight)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	# training arguments
	parser.add_argument("--train", default=None,
						help="Train text file")
	parser.add_argument("--save-net", default="lbl.hdf5", dest="save_net",
						help="File to save trained model")

	# evaluating arguments
	parser.add_argument("--ppl", default=None,
						help="Computes PPL of net on text file (if we train, do that after training)")
	parser.add_argument("--net", default=None,
						help="Net file to load")
	parser.add_argument("--arpa", metavar="FILE weight", default=None, nargs=2,
						help="ARPA n-gram model with interpolating, weight as second parameter")

	# common
	parser.add_argument("--alg", default="LBL", choices=["LBL", "HLBL", "LBL_MP"],
						help="Algorithm")
						
	args = parser.parse_args()

	if args.train:
		print("{0} algorithm training".format(args.alg))
		train(args.alg, args.train, args.save_net)

	if args.ppl and args.net:
		print("{0} algorithm evaluating".format(args.alg))
		if args.arpa:
			arpalm = ArpaLM.ArpaLM(args.arpa[0])
			weight = float(args.arpa[1])
			evaluate(args.alg, args.ppl, args.net, arpalm, weight)
		else:
			evaluate(args.alg, args.ppl, args.net)
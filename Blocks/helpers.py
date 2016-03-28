import toml

def readParams(filename):
	with open(filename) as f:
		return toml.loads(f.read())

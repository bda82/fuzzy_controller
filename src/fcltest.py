import fuzzy.storage.fcl.Reader as rd
reader = rd.Reader()
system = reader.load_from_file("model.fcl")

inp = {
    "wind": 60,
    "state_in": 10
}

out = {
    "state_out": 0.0
}

#--> old --> system.calculate(inp, out)
system.reset()
system.fuzzify(inp)
system.inference()
deff = system.defuzzify(out)

print 'deff'
print deff

print 'vars["state_out"]'
vars = system.variables
print vars["state_out"]

print '__repr__'
res = system.__repr__()
print res

print 'out["state_out"]'
state_out = out["state_out"]

print (u"state_out = {0}".format(state_out))


# What is this?

It's a small python project which enables reading [MFMC](https://github.com/ndtatbristol/mfmc) files.
Please note that despite there being a `write` directory, this doesn't yet support 
writing such files.

# How to use

This is a simple layer on top of [h5py](https://docs.h5py.org/en/stable/index.html).

Firstly, create a reader object using the `mfmc.FileReader` class.
An optional top-level group path can be passed.
Using this reader object, the contained *probe* and *sequence* data can be returned 
using the relevant properties.
The returned dictionary maps the name of the group which represents these objects to 
the objects themselves.
Once you're done with the reader, close it with `close()`.
File reader objects can also be used inside a context manager for automatic file 
closing.

Probes and sequences provide dictionary like access to their members as specified in 
the MFMC specification.
Names of fields can be provided in any case form, not just UPPER CASE.
If a required data field is not included in a probe, sequence or law object, an 
exception is raised.

Data fields which are not specified in the specification can be accessed as *user 
defined fields*, using the `user_datasets` and `user_attributes` properties.
They cannot be accessed using the normal dictionary interface, as an exception will 
be raised.
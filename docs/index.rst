Dibble
======

.. module:: dibble

Dibble is a small MongoDB Document Object Mapper.

Dibble depends on the `pymongo`_ module.

Features
--------

- Wrap MongoDB documents into Model objects
- Provide atomic update operations
- Update documents using atomic update operations
- Nested fields

Installation
------------

Install dibble with `pip`::

    $ pip install dibble

Or using `easy_install`::

    $ easy_install dibble

.. _pymongo: https://github.com/mongodb/mongo-python-driver

Defining Models
---------------

Models describe the structure of your MongoDB documents. Simply inherit from :class:`~dibble.model.Model` and define
fields according to your data schema::

    from dibble.model import Model
    from dibble.field import Field

    class MyModel(Model):
        myfield = Field()

Using Mappers
-------------

A model is by itself not really useful yet. To be able to save it into a collection, you must define a mapper. Mappers
are dibble's way of managing the relationship between models and collections.

It is recommended to subclass :class:`dibble.mapper.ModelMapper` and implement retrieval business logic in the
subclass::

    from dibble.mapper import ModelMapper

    class MyMapper(ModelMapper):
        # magic lives here
        ...

    mapper = MyMapper(MyModel, some_collection)

Creating new Model instances
----------------------------

To actually create documents and save data, request a new model instances from our mapper by calling it::

    model = mapper()

This is the most basic form to create new model instances. It is also possible to set initial data by providing a dict::

    model = mapper({'myfield': 'some data'})

Initial data may also be provided via kwargs or a combination of dict and kwargs (like the `dict` factory)::

    model = mapper(myfield='some data')
    model = mapper({'myfield': 'some data'}, myotherfield='some other data')

Accessing field values
----------------------

There are multiple ways to access the value of a field. The most straight-forward may be via the
:attr:`~dibble.fields.Field.value` attribute::

    val = model.myfield.value

Fields can also be called to get their value::

    val = model.myfield()

Or you may use dict-like access of the model, which always returns values instead of fields::

    val = model['myfield']

All of the above ways have identical results.

Manipulating Models
-------------------

Dibble's :class:`~dibble.fields.Field` class supports most MongoDB atomic update operations::

    model.myfield.set('updated data')

For a list of all available atomic operations, see :class:`~dibble.fields.Field`.

Saving Models
-------------

After you've done your data manipulations, you want to persist your changes. To do this, simply call
:meth:`~dibble.model.Model.save` on the model instance::

    model.save()

Dibble defaults to safe=True, but that can be overridden this by passing safe=False::

    model.save(safe=False)

In any case :meth:`~dibble.model.Model.save` returns the ObjectId of the document.

Retrieving Documents
--------------------

Mappers can be used pretty much like a :class:`pymongo.collection.Collection` to retrieve documents from your
collection.

You may retrieve single documents::

    model = mapper.find_one({'myfield': 'something'})

Or you may retrieve a cursor of documents::

    models = mapper.find({'myfield': 'some other thing'})

Cursors have all the standard methods you would expect for a :class:`pymongo.cursor.Cursor` for sorting and limiting
results::

    models.count()
    models.skip(5).limit(10).sort('myotherfield', -1)

Updating multiple documents
---------------------------

For updating multiple documents based on a query document simply use the :meth:`~dibble.mapper.ModelMapper.update`
method of the mapper. This method simply proxies to :meth:`pymongo.collection.Collection.update`.

API Reference
-------------

.. module:: dibble.model
.. autoclass:: Model
    :members:
    :inherited-members:

.. module:: dibble.fields
.. autoclass:: Field
    :members:
    :inherited-members:

.. module:: dibble.mapper
.. autoclass:: ModelMapper
    :members:

    .. automethod:: __call__


===============
Pandas-Bikeshed
===============


This is a fine selection of random useful or useless code and helper functions collected to simplify my life with the great pandas.


Installation
------------
As of now I do not recommend the installation in a production environment. 

Therefore cloning the environment and using ``pip install --editable`` is recommended for your testing endavours into the pandas-bikeshed

If you simply want to give it a go in your virtual environment run::

    pip install git+https://github.com/sholderbach/pandasbikeshed.git@master


Features
--------

Fast and easy conditional indexing into pd.DataFrames and pd.Series using the pandasbikeshed.fancyfilter utilities.

Just import the small accessor ``me`` via::

    from pandasbikeshed.fancyfilter import me

now you can do::

    my_long_dataset_name.loc[me.cost > 500,['name', 'product_id']]

instead of e.g.::

    my_long_dataset_name.loc[my_long_dataset_name.cost > 500,['name', 'product_id']]

As you don't have to store an intermediate DataFrame or boolean masks seperately it is very useful for method chaining pipelines.

e.g.::

    df = ... # Some tidy table with order, customer and shipment information
    query_customers = [...] # Some customers we want to query
    count_unique = lambda x: x.nunique()
    analysis = (df.loc[(me.customer.isin(query_customers)) & (me.order == 'active')]
                .groupby('shipment')
                .agg(items=('id', 'count'),
                    cost=('item_prize', 'sum'),
                    num_customers=('customer', count_unique),
                    num_destinations=('city', count_unique))
                .loc[me.num_customers > 1]
                .sort_values(by='cost'))

Currently implemented are the standard python comparison operators (``<``, ``<=``, ``==``, ``!=``, ``>=``, ``>``) ``.isin`` (to select all entries that are present in a list passed to ``.isin``) and logical chaining with ``&``, ``|`` and ``^`` as well as convenience functions for ``.isna`` and a ``np.isfinite`` like check.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

# Reinforcement Learning

* Instead of normalizing the GDP (which does not have an upperbound), we can just scale the death rate with the _GDP_
    * This can be done by taking `max_death_rate - death_rate` (a value between _0_ and _1_ that we want to maximize) and the _GDP_
    * We then multiply the two values to get our reward
        * You cannot maximize only one, e.g. focusing on _GDP_ only and letting the _death_rate_ go to _0_, will result in the minimum reward of _0_
        * Maximizing one makes it more valuable to maximize the other, e.g. if _GDP_ is _10_, then lowering the _death_rate_ from _0.2_ to _0.1_ will gain you _1_ more unit for the reward, whereas if the _GDP_ is _100_ the same change in _death_rate_ will gain you _10_ units
        
* _GDP_ testing
    * Try to make _GDP_ go down
        * Examples of things one can do
            * Artificially keep the _death_rate_ to _90%_
            * Set _alpha_ to _1.0_
        * You should see the _GDP_ inevitably go down cause the cards are stacked agains the nations
        
# Simulation

* Add noise to air migrations
    * Assume Gaussian distribution
        * What parameters to use?
            * The _mean_ is the value you are currently using (on average it should be close to that)
            * The _variance_ 
                * The best option is to have the _std_ be a percentage of the _mean_ (see example below)
                * Can manually set to a low value to add a bit of noise
                * Can be set to the actual variance of the data
                    * Not really adviseable because there aren't enough values
                    * This can be used as an _inspiration_ to set a manual value
        * How to apply the noise?
            * we have a value `X` is Normally distributed, with _mean_ `m` and _variance_ `d`, hence `X~N(m,d)`
            * this is the same as taking the Normal distribution with _mean_ _0_ and variance _1_, and then scaling it by `d` and shifting it by `m`
            * in other words, `X~N(m,d)` is the same as saying `X = m + d*e` where `e~N(0,1)`
            * you can do this in `numpy` with the following function
            ```python
            import numpy as np
            def add_noise(mean, percentace_std):
                return mean + np.random.normal(scale=percentage_std*mean, size=1)
            ```
            where `np.random.normal(1)` will sample _1_ value from `N(0,1)`, and `size=1` because `mean` is a value (_float_) and not an array, otherwise I can do `size=mean.shape`
        
        

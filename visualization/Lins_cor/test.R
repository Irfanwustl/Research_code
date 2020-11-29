library(DescTools)
# NOT RUN {
## Concordance correlation plot:
set.seed(seed = 1234)
method1 <- rnorm(n = 100, mean = 0, sd = 1)
method2 <- method1 + runif(n = 100, min = 0, max = 1)

## Introduce some missing values:


tmp.ccc <- CCC(method1, method2, ci = "z-transform",
               conf.level = 0.95)

tmp.ccc$rho.c
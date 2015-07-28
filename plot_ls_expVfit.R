require(ggplot2)

DFDIR <- '~/Documents/drilling/analyses/all/output/'
FIGDIR <- '~/Documents/drilling/analyses/all/figs/'

EXPNAME <- 'bayesOpt_e'
EXPDATE <- '072215'

NAME <- paste('df_lsfit_regret', EXPNAME, EXPDATE, sep='_')

df <- read.csv(paste(DFDIR, NAME, '.csv', sep=''), header=TRUE)

df$cond <- as.factor(df$exp_ls)

# drop pandas residue
df <- subset(df, select=-c(X))

# log-transform data
df$fit_ls <- log2(df$fit_ls)
df$exp_ls <- log2(df$exp_ls)

model <- lm(fit_ls ~ exp_ls, data=df)
grid <- with(df, expand.grid(
    exp_ls=seq(-8, 0, length=101)))

err <- stats::predict(model, newdata=grid, se = TRUE)
grid$ucl <- err$fit + 1.96 * err$se.fit
grid$lcl <- err$fit - 1.96 * err$se.fit
grid$fit_ls <- err$fit


# b3 <- ggplot(data=df2, aes(x=fit_lenscale, y=exp_lenscale)) + stat_density(aes(ymax = ..density.., ymin = -..density.., 
#     fill = cond), geom = "ribbon", position = "identity") + coord_flip()

xlab = expression(paste('optimal lengthscale ('*2^'x'*')'))
ylab = expression(paste('fit lengthscale ('*2^'y'*')'))

ggp <- ggplot(aes(x=exp_ls, y=fit_ls), data=df)
ggp +
    geom_abline(intercept=0,
                slope=1,
                linetype='dashed',
                colour='red') +
#     geom_smooth(aes(ymin=lcl,
#                     ymax=ucl,
#                     y=fit_ls),
#                 colour='black',
#                 data=grid,
#                 stat='identity') +
    geom_boxplot(aes(group=cond,
                     x=exp_ls,
                     y=fit_ls),
                 width=0.4,
                 colour='black',
                 fill=NA,
                 outlier.shape=NA,
                 data=df) + 
    geom_point(position=position_jitter(width=0.2),
               alpha=0.2,
               size=4) +
#     scale_y_continuous(breaks=seq(-10, 0, 2),
#                        limits=c(-9, -1)) +  # Ticks from -8 to -2, every 2
#     scale_x_continuous(breaks=seq(-6, -2, 2),
#                        limits=c(-7, -1)) + # Ticks from -6 to -2, every 2
    labs(x=xlab,
         y=ylab) +
    ggtitle('Optimal versus Fit Lengthscale') +
    theme_light() +
    theme(panel.border = element_blank())

ggsave(paste(FIGDIR, NAME, '.pdf', sep=''))

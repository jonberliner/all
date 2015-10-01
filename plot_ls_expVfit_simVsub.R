require(ggplot2)

FIGDIR <- '~/Documents/drilling/analyses/all/figs/'

DFDIR <- '~/Desktop/'
EXPNAME <- 'SIM_bayesOpt_e'
EXPDATE <- '073115'
NAME <- paste('df_lsfit_regret', EXPNAME, EXPDATE, sep='_')
df_sim <- read.csv(paste(DFDIR, NAME, '.csv', sep=''), header=TRUE)
df_sim$cond <- as.factor(df_sim$exp_ls)
# drop pandas residue
df_sim <- subset(df_sim, select=-c(X))
# log-transform data
df_sim$fit_ls <- log2(df_sim$fit_ls)
df_sim$exp_ls <- log2(df_sim$exp_ls)
df_sim$suborsim <- 'sim'

DFDIR <- '~/Documents/drilling/analyses/all/output/'
EXPNAME <- 'bayesOpt_e'
EXPDATE <- '072215'
NAME <- paste('df_lsfit_regret', EXPNAME, EXPDATE, sep='_')
df_sub <- read.csv(paste(DFDIR, NAME, '.csv', sep=''), header=TRUE)
df_sub$cond <- as.factor(df_sub$exp_ls)
# drop pandas residue
df_sub <- subset(df_sub, select=-c(X))
# log-transform data
df_sub$fit_ls <- log2(df_sub$fit_ls)
df_sub$exp_ls <- log2(df_sub$exp_ls)
df_sub$suborsim <- 'sub'

myvars <- c("sse", "fit_ls", "exp_ls", "workerid", "suborsim", "cond", "counterbalance")
df_sim <- df_sim[,myvars]
df_sub <- df_sub[,myvars]

df <- rbind(df_sub, df_sim)

ggp <- ggplot(aes(x=exp_ls, y=sse, colour=suborsim), data=df)



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
# ylab = expression(paste('fit lengthscale ('*2^'y'*')'))
ylab = expression(paste('goodness of fit (summed regret)'))

ggp <- ggplot(aes(x=exp_ls, y=sse), data=df)
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
    ggtitle('Optimal versus Fit Lengthscale\n for Random Data') +
    theme_light() +
    theme(panel.border = element_blank())

ggsave(paste(FIGDIR, NAME, '.pdf', sep=''))

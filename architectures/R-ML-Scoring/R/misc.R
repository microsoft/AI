run("rm ../bffs/data/forecasts/*")

run("ls -l ../bffs/data/forecasts | wc -l")

run("ls ../bffs/data/forecasts")


job <-"job20190127214222"

getJobFile(job, "1", "wd/1.txt")
getJobFile(job, "1", "stderr.txt")
getJobFile(job, "1", "stdout.txt")

dat %>%
  filter(sku == 1, store == 1) %>%
  filter(week>=80) %>%
  select(week, sales) %>%
  ggplot(aes(x = week, y = sales)) +
  geom_line(colour = "blue", size = 0.5) +
  scale_y_log10() +
  theme(axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.line = element_line(size = 0.25, colour = "blue"),
        axis.text = element_blank(),
        axis.ticks = element_blank(),
        panel.grid = element_blank()) +
  ggsave("ts.png", device = "png", width = 1, height = 1)
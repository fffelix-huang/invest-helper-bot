from redisworks import Root

root = Root()


def add_watch_list(user_id, stock):
    watch_list = root[user_id + "-watch-list"]
    if stock not in watch_list:
        watch_list.append(stock)

    return watch_list

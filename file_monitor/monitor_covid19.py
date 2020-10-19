import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, RegexMatchingEventHandler


watch_patterns = "*.csv"
# watch_patterns = [r'^.+\.csv$']
ignore_patterns = ""
ignore_directories = False
case_sensitive = True


def on_created(event):
    print(f"{event.src_path} 被创建")


def on_deleted(event):
    print(f"{event.src_path} 被删除")


def on_modified(event):
    print(f"{event.src_path} 被修改")


def on_moved(event):
    print(f"{event.src_path} 被移动到 {event.dest_path}")


def main():
    event_handler = PatternMatchingEventHandler(
        watch_patterns, ignore_patterns, ignore_directories, case_sensitive)

    # event_handler = RegexMatchingEventHandler(
    #     watch_patterns, [], ignore_directories, case_sensitive)

    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_moved = on_moved
    event_handler.on_modified = on_modified

    go_recursively = True    # 是否监控子文件夹
    covid19_observer = Observer()
    watch_path = "/Users/mac/Learning/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/"  # 监控目录
    covid19_observer.schedule(event_handler, watch_path, recursive=go_recursively)

    covid19_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        covid19_observer.stop()
        covid19_observer.join()


if __name__ == '__main__':
    main()

#include <queue>

using std::queue;

class Producer {
private:
  queue<statu> process_queue;
  int lock;
public:
  statu & getTask();
  bool taskDone(statu & task);
};


const LinkedList = require("./LinkedList");

class Queue{
    constructor(maxSize = Infinity)
    {
        this.size = 0
        this.Queue = new LinkedList();
        this.maxSize = maxSize;
    }
    isEmpty()
    {
        return this.size === 0;
    }
    hasRoom()
    {
        return this.size < this.maxSize;
    }

    enqueue(data)
    {
        if(this.hasRoom())
        {
            this.Queue.addToTail(data);
            this.size += 1;

        }
        else
        {
            throw new Error("Queue is full!");
        }
    }

    dequeue()
    {
        if(!this.isEmpty())
        {
            const data = this.Queue.removeHead();
            this.size -= 1;
            return data;
        }
        else
        {
            throw new Error("Queue is Empty!");
        }
    }
}

module.exports = Queue;
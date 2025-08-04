class MinHeap
{
    constructor()
    {
        this.heap = [null];
        this.size = 0;

    }

    popMin()
    {
        if(this.size === 0 )
        {
            return null;
        }
        const min = this.heap[1];
        this.heap[1] = this.heap[this.size];
        this.heap.pop();
        this.size -= 1;
        this.heap();
        return min;
    }

    add(value)
    {

    }

    bubbleUp() //Smaller values go to the top of the heap whilst the bigger values move down
    {

    }

    heap()
    {

    }
}

const getParent = current => Math.floor((current/2));
const getLeft = current => current*2;
const getRight = current => current * 2 + 1;
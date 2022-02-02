class Node{
    constructor(data)
    {
        this.data = data;
        this.next = null;
        this.previous = null;
    }
    setNextNode(node){
        if(node instanceof Node || node === null)
        {
            this.next = node;
        }
        else
        {
            throw new Error('Input an instance of Node');
        }
    }
    setPreviousNode(node) {
        if (node instanceof Node || node === null) {
          this.previous = node;
        } else {
          throw new Error('Previous node must be a member of the Node class')
        }
      }
    getNextNode()
    {
        return this.next;
    }
    getPreviousNode() {
        return this.previous;
      }
}

module.exports = Node;
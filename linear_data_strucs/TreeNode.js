class TreeNode{
    constructor(data)
    {
        this.data = data;
        this.children = [];
    }

    addChild(data)
    {
        if(data instanceof TreeNode)
        {
            this.children.push(data);
        }
        else
        {
            this.children.push(new TreeNode(data));
        }
    }

    removeChild(data)
    {
        const length = this.children.length;
        this.children = this.children.filter(child => {
            if (data instanceof TreeNode)
            {
                if(data !== child)
                {
                    return true;
                }
                else
                {
                    return false;
                }
                }
            else
            {
                if(childToRemove !== child.data)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        })

        if(length === this.children.length)
        {
            this.children.forEach(child => child.removeChild(childToRemove));
        }
    };

    
}

const abc = new TreeNode('alpha');

console.log(abc);

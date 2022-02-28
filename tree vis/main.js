class Node{  
    constructor(data)
    {
        this.val = data;
        this.left = null;
        this.right = null;
    }
  };
  
  class BST{
    constructor(root = null){
      this.root = root;
    }
  
    insert(value){
      let node = this.root
      if(!node){
        this.root = new Node(value);
      }
      else{
        const recursive = function(data) {
          if(value < data.val)
          {
            if(data.left === null)
            {
              data.left = new Node(value);
              return;
            }
            else if(data.left !== null)
            {
              return recursive(data.left);
            }
          }
          else if(value > data.val){
            if(data.right === null)
            {
              data.right = new Node(value);
              return
            }
            else if(data.right !== null)
            {
              return recursive(data.right);
            }
          }
          else{
            return null;
          }
        }
        return recursive(node);
      }
    }
  
    remove(data){
      this.root = this.removeNode(this.root, data);
    }
  
    removeNode(node,data){
      if(node === null){
        return null;
      }
      else if(data < node.val)
      {
        node.left = this.removeNode(node.left,data);
        return node;
      }
      else if(data > node.val)
      {
        node.right = this.removeNode(node.right,data);
        return node;
      }
      else{
        if(!node.left && !node.right){
          node = null;
          return node;
        }
        else if(!node.left){
          node = node.right;
          return node;
        }
        else if(!node.right){
          node = node.left;
          return node;
        }
  
          let temp = this.findMin(node.right);
          node.val = temp.val;
  
          node.right = this.removeNode(node.right,temp.val);
          return node;
      }
    }
  
    findMin(node){
      if(node.left === null)
      {
        return node;
      }
      else{
        return this.findMin(node.left);
      }
    }
  }
  


const renderTree = (node) => {
    if(node.left && node.right){
        return `<ul>
        <li>
            <div> ${node.val} </div>
            <ul>
                <li>
                    <div> ${renderTree(node.left)}</div>
                </li>
                <li>
                    <div> ${renderTree(node.right)}</div>
                </li>
            </ul>
                        
        </li>
    </ul>`
    }
    else if(!node.left && node.right){
        return `<ul>
        <li>
            <div> ${node.val} </div>
            <ul>
                <li>
                    <div> - </div>
                </li>
                <li>
                    <div> ${renderTree(node.right)} </div>
                </li>
            </ul>
                        
        </li>
    </ul>`
    }
    else if(node.left && !node.right)
    {
        return `<ul>
        <li>
            <div> ${node.val} </div>
            <ul>
                <li>
                    <div> ${renderTree(node.left)}</div>
                </li>
                <li>
                    <div> - </div>
                </li>
            </ul>
                        
        </li>
    </ul>`
    }
    else if(!node.left && !node.right){
        return `<ul>
        <li>
            <div> ${node.val} </div>                        
        </li>
    </ul>`
    }
    else{
        return null;
    }
}

/*
const renderTree = (node) => {
    if(!node.val) {
        return
    }
    else{
                return `<ul>
            <li>
                <div> ${node.val} </div>
                    ${node.left || node.right ? (`<ul>
                    <li>
                        <div> ${renderTree(abc.root.left)} </div>
                    </li>
                    <li>
                        <div> Yes</div>
                    </li>
                </ul>`) : ''}
                    
                            
            </li>
        </ul>`
    }
    
} */

const input = document.getElementById('input');
const add = document.getElementById('add');
add.addEventListener('click',addValue);
const remove = document.getElementById('remove');
remove.addEventListener('click',removeValue);
const treeEles = document.querySelector('.tree')


const abc = new BST();
abc.insert(15);
abc.insert(25);
abc.insert(10);
abc.insert(7);
abc.insert(22);
abc.insert(17);
abc.insert(13);
abc.insert(5);
abc.insert(9);
abc.insert(27);
console.log(abc.root);

console.log(renderTree(abc.root));

const main = () =>{

    treeEles.innerHTML = renderTree(abc.root);
}

function addValue(){
  let temp = input.value;
  console.log(temp);
  abc.insert(temp);
  treeEles.innerHTML = renderTree(abc.root);
  input.value = '';
};

function removeValue(){
  let temp = input.value;
  abc.remove(temp);
  treeEles.innerHTML = renderTree(abc.root);
  input.value = '';
};

main(); 
<script>
    
    export let type = 'primary';
    export let flat = false;
    export let inverse = false;
    export let handleClick;
    export let goToUrl;

    const handleClickWrapper = () => {
    handleClick(goToUrl);
    };

</script>

<button class={type} on:click={handleClickWrapper}>
    <slot></slot>
</button>

<style>
    button{
        border: 1;
        cursor: pointer;
        border-radius: 6px;
        padding: 8px 12px;
        font-weight: light;
        box-shadow: 1px, 2px, 3px rgba(0, 0, 0, 0.2)
    }
    .primary{
        display: inline-block;
        outline: 0;
        cursor: pointer;
        border: 1px solid #000;
        color: #000;
        background: #fff;
        font-size: 20px;
        font-weight: 200;
        line-height: 28px;
        padding: 12px 20px;
        text-align:center;
        transition-duration: .15s;
        transition-property: all;
        transition-timing-function: cubic-bezier(.4,0,.2,1);
    }  
    .primary:hover{
        background: rgb(0, 170, 255);
        color: white;
    }

    .secondary {
        align-items: center;
        appearance: none;
        background-color: #FCFCFD;
        border-radius: 4px;
        border-width: 0;
        box-shadow: rgba(45, 35, 66, 0.4) 0 2px 4px,rgba(45, 35, 66, 0.3) 0 7px 13px -3px,#D6D6E7 0 -3px 0 inset;
        box-sizing: border-box;
        color: #36395A;
        cursor: pointer;
        display: inline-flex;
        height: 48px;
        justify-content: center;
        line-height: 1;
        list-style: none;
        overflow: hidden;
        padding-left: 16px;
        padding-right: 16px;
        position: relative;
        text-align: left;
        text-decoration: none;
        transition: box-shadow .15s,transform .15s;
        user-select: none;
        -webkit-user-select: none;
        touch-action: manipulation;
        white-space: nowrap;
        will-change: box-shadow,transform;
        font-size: 18px;
    }

    .secondary:focus {
        box-shadow: #D6D6E7 0 0 0 1.5px inset, rgba(45, 35, 66, 0.4) 0 2px 4px, rgba(45, 35, 66, 0.3) 0 7px 13px -3px, #D6D6E7 0 -3px 0 inset;
    }

    .secondary:hover {
        box-shadow: rgba(45, 35, 66, 0.4) 0 4px 8px, rgba(45, 35, 66, 0.3) 0 7px 13px -3px, #D6D6E7 0 -3px 0 inset;
        transform: translateY(-2px);
    }

    .secondary:active {
        box-shadow: #D6D6E7 0 3px 7px inset;
        transform: translateY(2px);
    }
</style>
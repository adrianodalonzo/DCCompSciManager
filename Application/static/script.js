const addMemberBtn = document.getElementById('add_member_btn')
const deleteMemberBtn = document.getElementById('delete_member_btn')
const blockMemberBtn = document.getElementById('block_member_btn')

addMemberBtn.addEventListener('click', () => {
    const form = document.getElementById('add_member')
    if (form.style.display == 'block') {
        document.getElementById('add_member').style.display = 'none'
    } else {
        document.getElementById('add_member').style.display = 'block'
    }
})

deleteMemberBtn.addEventListener('click', () => {
    const form = document.getElementById('delete_member')
    if (form.style.display == 'block') {
        document.getElementById('delete_member').style.display = 'none'
    } else {
        document.getElementById('delete_member').style.display = 'block'
    }
})

blockMemberBtn.addEventListener('click', () => {
    const form = document.getElementById('block_member')
    if (form.style.display == 'block') {
        document.getElementById('block_member').style.display = 'none'
    } else {
        document.getElementById('block_member').style.display = 'block'
    }
})
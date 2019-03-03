const Menu = [
  { header: 'Apps' },
  {
    title: 'Dashboard',
    group: 'apps',
    icon: 'dashboard',
    name: 'Dashboard',
    href: '/dashboard'
  },
  {
    title: 'Numbers',
    group: 'apps',
    icon: 'phone_android',
    name: 'Numbers',
    href: '/numbers'
  },
  {
    title: 'Messages',
    group: 'apps',
    icon: 'chat',
    name: 'Messages',
    items: [
      { name: "Create", title: "Create", href: "/messages/create" },
      { name: "Inbox", title: "Inbox", href: "/messages/inbox" },
      { name: "Outbox", title: "Outbox", href: "/messages/outbox" }
    ]
  },
  {
    title: 'Contacts',
    group: 'apps',
    icon: 'contacts',
    name: 'Contacts',
    href: '/contacts'
  },
  {
    title: 'Media',
    group: 'apps',
    icon: 'perm_media',
    name: 'Media',
    href: '/media'
  }
];
// reorder menu
Menu.forEach((item) => {
  if (item.items) {
    item.items.sort((x, y) => {
      let textA = x.title.toUpperCase();
      let textB = y.title.toUpperCase();
      return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
    });
  }
});

export default Menu;

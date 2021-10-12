var data = {
  startTime: 1540310400,
  endTIme: 1533225600,
  total: 4000,
  nodes: {
    id: 'BABA',
    time: '',
    children: [{
      parentId: 'BABA',
      id: 'A',
      time: '2018-10-24',
      value: 3600,
      children: [
        {
          parentId: 'A',
          id: 'A-1',
          time: '2018-10-25',
          value: 100,
          children: [
            {
              parentId: 'A-1',
              id: 'O-1',
              time: '2018-10-26',
              value: 50,
            }, {
              parentId: 'A-1',
              id: 'O-2',
              time: '2018-11-05',
              value: 50,
            }
          ]
        }, {
          parentId: 'A',
          id: 'A-2',
          time: '2018-10-26',
          value: 1100,
          children: [
            {
              parentId: 'A-2',
              id: 'B-1',
              time: '2018-10-27',
              value: 400,
              children: [
                {
                  parentId: 'B-1',
                  id: 'C-1',
                  time: '2018-10-28',
                  value: 200,
                  children: [
                    {
                      parentId: 'C-1',
                      id: 'D-1',
                      time: '2018-10-30',
                      value: 100,
                    }, {
                      parentId: 'C-1',
                      id: 'D-2',
                      time: '2018-11-05',
                      value: 100,
                    }
                  ]
                }, {
                  parentId: 'B-1',
                  id: 'C-2',
                  time: '2018-10-29',
                  value: 200,
                }
              ]
            }, {
              parentId: 'A-2',
              id: 'B-2',
              time: '2018-10-27',
              value: 400,
              children: [
                {
                  parentId: 'B-2',
                  id: 'K-1',
                  time: '2018-10-30',
                  value: 100,
                }, {
                  parentId: 'B-2',
                  id: 'K-2',
                  time: '2018-11-05',
                  value: 300,
                }
              ]
            }, {
              parentId: 'A-2',
              id: 'B-3',
              time: '2018-10-28',
              value: 200,
            }, {
              parentId: 'A-2',
              id: 'B-4',
              time: '2018-10-29',
              value: 100,
              children: [
                {
                  parentId: 'B-4',
                  id: 'L-1',
                  time: '2018-10-30',
                  value: 50,
                }, {
                  parentId: 'B-4',
                  id: 'L-2',
                  time: '2018-11-05',
                  value: 50,
                }
              ]
            }
          ]
        }, {
          parentId: 'A',
          id: 'A-3',
          time: '2018-10-27',
          value: 300,
        }, {
          parentId: 'A',
          id: 'A-4',
          time: '2018-10-25',
          value: 900,
        }, {
          parentId: 'A',
          id: 'A-5',
          time: '2018-10-26',
          value: 600,
        }, {
          parentId: 'A',
          id: 'A-6',
          time: '2018-10-27',
          value: 600,
        },
      ]
    },
      {
        parentId: 'BABA',
        id: 'P',
        time: '2018-10-24',
        value: 400,
        children: [
          {
            parentId: 'P',
            id: 'P-1',
            time: '2018-10-25',
            value: 100,
          }, {
            parentId: 'P',
            id: 'P-2',
            time: '2018-10-26',
            value: 300,
          }]
      }]
  }
}